from datetime import datetime, timedelta
from typing import Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.services import user_service
from app.models.user import User, UserRole


security = HTTPBearer()


class TokenData:
    def __init__(self, username: Optional[str] = None):
        self.username = username


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify JWT token and return username"""
    token = credentials.credentials
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data.username


async def get_current_user(
    username: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    user = await user_service.get_user_by_username(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuário inativo"
        )
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operação não permitida para este tipo de usuário"
            )
        return current_user


# Dependências específicas para diferentes roles
require_admin = RoleChecker([UserRole.ADMIN])
require_admin_or_vendas = RoleChecker([UserRole.ADMIN, UserRole.VENDAS])


class PermissionChecker:
    @staticmethod
    def can_modify_user(current_user: User, target_user_id: int) -> bool:
        """Check if user can modify another user"""
        # Admin can modify anyone
        if current_user.role == UserRole.ADMIN:
            return True
        
        # Users can only modify themselves
        return current_user.id == target_user_id
    
    @staticmethod
    def can_view_user(current_user: User, target_user_id: int) -> bool:
        """Check if user can view another user"""
        # Admin can view anyone
        if current_user.role == UserRole.ADMIN:
            return True
        
        # Users can only view themselves
        return current_user.id == target_user_id
    
    @staticmethod
    def can_delete_user(current_user: User, target_user_id: int) -> bool:
        """Check if user can delete another user"""
        # Only admin can delete users
        if current_user.role != UserRole.ADMIN:
            return False
        
        # Admin cannot delete themselves
        return current_user.id != target_user_id


def check_user_permission(target_user_id: int):
    """Check if current user has permission to access target user"""
    async def _check_permission(current_user: User = Depends(get_current_active_user)):
        if not PermissionChecker.can_view_user(current_user, target_user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este usuário"
            )
        return current_user
    return _check_permission


def check_modify_permission(target_user_id: int):
    """Check if current user has permission to modify target user"""
    async def _check_permission(current_user: User = Depends(get_current_active_user)):
        if not PermissionChecker.can_modify_user(current_user, target_user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para modificar este usuário"
            )
        return current_user
    return _check_permission


def check_delete_permission(target_user_id: int):
    """Check if current user has permission to delete target user"""
    async def _check_permission(current_user: User = Depends(get_current_active_user)):
        if not PermissionChecker.can_delete_user(current_user, target_user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar este usuário"
            )
        return current_user
    return _check_permission
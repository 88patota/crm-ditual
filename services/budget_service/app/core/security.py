"""
Autenticação e segurança para o Budget Service
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Configurações JWT (devem ser as mesmas do user_service)
SECRET_KEY = "your-secret-key-here"  # Mesma chave do user_service
ALGORITHM = "HS256"

security = HTTPBearer()


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class CurrentUser(BaseModel):
    username: str
    role: str


def verify_token(token: str) -> Optional[TokenData]:
    """Verificar e decodificar token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        # Obter role do payload
        role = payload.get("role", "vendas")  # Default para vendas se não especificado
        
        return TokenData(username=username, role=role)
    except JWTError as e:
        # Log do erro para debug
        print(f"JWT Error: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """Obter usuário atual a partir do token JWT"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(credentials.credentials)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    
    return CurrentUser(username=token_data.username, role=token_data.role or "vendas")


async def get_current_active_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """Obter usuário ativo atual"""
    # Em produção, você pode adicionar verificações adicionais aqui
    return current_user


def require_admin(current_user: CurrentUser = Depends(get_current_active_user)) -> CurrentUser:
    """Dependency que requer privilégios de administrador"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user


def get_user_filter(current_user: CurrentUser = Depends(get_current_active_user)) -> Optional[str]:
    """
    Retorna filtro de usuário baseado no role:
    - Admin: None (vê todos os orçamentos)
    - Vendas: username (vê apenas seus orçamentos)
    """
    if current_user.role == "admin":
        return None  # Admin vê todos
    else:
        return current_user.username  # Vendas vê apenas os seus

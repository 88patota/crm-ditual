from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import (
    get_current_active_user, 
    require_admin, 
    require_admin_or_vendas,
    check_user_permission,
    check_modify_permission,
    check_delete_permission
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserLogin, Token, UserSelfUpdate, UserMe, PasswordUpdate
from app.services import user_service
from app.services.auth import create_access_token
from app.services.messaging import publish_user_created, publish_user_updated, publish_user_deleted, publish_user_login
from app.core.config import settings
from app.models.user import User
from datetime import timedelta


router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Criar um novo usuário (apenas administradores)"""
    # Verificar se usuário já existe
    existing_user = await user_service.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso"
        )
    
    existing_email = await user_service.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    user = await user_service.create_user(db, user_data)
    
    # Publicar evento de usuário criado
    user_dict = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role.value,
        "is_active": user.is_active,
        "created_by": current_user.username
    }
    await publish_user_created(user_dict)
    
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Listar usuários com paginação (apenas administradores)"""
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=UserMe)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Obter perfil do usuário atual"""
    return current_user


@router.put("/me", response_model=UserMe)
async def update_current_user_profile(
    user_data: UserSelfUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualizar perfil do usuário atual (campos limitados)"""
    # Verificar se username já existe (se fornecido)
    if user_data.username and user_data.username != current_user.username:
        existing_user = await user_service.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso"
            )
    
    # Verificar se email já existe (se fornecido)
    if user_data.email and user_data.email != current_user.email:
        existing_email = await user_service.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
    
    # Converter para UserUpdate (sem role e is_active)
    update_data = UserUpdate(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name
    )
    
    user = await user_service.update_user(db, current_user.id, update_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Erro ao atualizar usuário"
        )
    
    # Publicar evento de usuário atualizado
    user_dict = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role.value,
        "is_active": user.is_active,
        "updated_by": current_user.username,
        "self_update": True
    }
    await publish_user_updated(user_dict)
    
    return user


@router.put("/me/password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Alterar senha do usuário atual"""
    from app.services.auth import verify_password, get_password_hash
    
    # Verificar senha atual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualizar senha
    new_password_hash = get_password_hash(password_data.new_password)
    
    # Criar uma versão especial de update apenas para senha
    from sqlalchemy import update
    from app.models.user import User as UserModel
    
    stmt = update(UserModel).where(UserModel.id == current_user.id).values(
        hashed_password=new_password_hash
    )
    
    await db.execute(stmt)
    await db.commit()
    
    return {"message": "Senha alterada com sucesso"}


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obter usuário por ID (usuários podem ver apenas seu próprio perfil, admin pode ver todos)"""
    # Verificar permissão
    from app.core.security import PermissionChecker
    if not PermissionChecker.can_view_user(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este usuário"
        )
    
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualizar usuário (usuários podem atualizar apenas seu próprio perfil, admin pode atualizar todos)"""
    # Verificar permissão
    from app.core.security import PermissionChecker
    if not PermissionChecker.can_modify_user(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para modificar este usuário"
        )
    
    user = await user_service.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Publicar evento de usuário atualizado
    user_dict = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role.value,
        "is_active": user.is_active,
        "updated_by": current_user.username
    }
    await publish_user_updated(user_dict)
    
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deletar usuário (soft delete - apenas administradores)"""
    # Verificar permissão
    from app.core.security import PermissionChecker
    if not PermissionChecker.can_delete_user(current_user, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este usuário"
        )
    
    success = await user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Publicar evento de usuário deletado
    await publish_user_deleted(user_id)


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Autenticar usuário e retornar token JWT"""
    user = await user_service.authenticate_user(
        db, user_credentials.username, user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Publicar evento de login
    user_dict = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role.value
    }
    await publish_user_login(user_dict)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Registro público de usuário (apenas perfil de vendas)"""
    from app.models.user import UserRole
    
    # Forçar role como vendas para registro público
    user_data.role = UserRole.VENDAS
    
    # Verificar se usuário já existe
    existing_user = await user_service.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso"
        )
    
    existing_email = await user_service.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    user = await user_service.create_user(db, user_data)
    
    # Publicar evento de usuário criado
    user_dict = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role.value,
        "is_active": user.is_active,
        "public_registration": True
    }
    await publish_user_created(user_dict)
    
    return user
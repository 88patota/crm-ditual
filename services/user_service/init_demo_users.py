#!/usr/bin/env python3
"""
Script para inicializar usuários demo no sistema
"""

import asyncio
import sys
import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.services.user_service import UserService
from app.schemas.user import UserCreate

# Adicionar o diretório app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def init_demo_users():
    """Inicializar usuários de demonstração"""
    async with get_db_session() as db:
        user_service = UserService(db)
        
        demo_users = [
            {
                "username": "admin",
                "email": "admin@crmditual.com",
                "password": "admin123",
                "full_name": "Administrador",
                "role": "admin",
                "is_active": True
            },
            {
                "username": "vendedor1",
                "email": "vendedor1@crmditual.com", 
                "password": "vendedor123",
                "full_name": "Vendedor Um",
                "role": "salesperson",
                "is_active": True
            }
        ]
        
        for user_data in demo_users:
            try:
                # Verificar se usuário já existe
                existing_user = await user_service.get_user_by_username(user_data["username"])
                
                if existing_user:
                    logger.info(f"User {user_data['username']} already exists, skipping")
                    continue
                
                # Criar novo usuário
                user_create = UserCreate(**user_data)
                new_user = await user_service.create_user(user_create)
                
                if new_user:
                    logger.info(f"User {user_data['username']} created successfully")
                else:
                    logger.error(f"Failed to create user {user_data['username']}")
                    
            except Exception as e:
                logger.error(f"Error creating user {user_data['username']}: {str(e)}")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        asyncio.run(create_demo_users())
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
Script para criar usuário admin no CRM Ditual
Funciona em ambiente Docker/EC2

Uso:
    python create_admin_user.py
    
Ou via docker-compose:
    docker-compose exec user_service python create_admin_user.py
"""

import asyncio
import sys
import os
import logging
from pathlib import Path
from sqlalchemy import text

# Adicionar o diretório app ao path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(app_dir))

try:
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.core.database import AsyncSessionLocal
    from app.services import user_service
    from app.schemas.user import UserCreate
    from app.models.user import UserRole
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    print("💡 Certifique-se de executar dentro do container user_service")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def create_admin_user():
    """Criar usuário admin no sistema"""
    
    print("🚀 Iniciando criação do usuário admin...")
    print("=" * 50)
    
    # Dados do usuário admin
    admin_data = {
        "username": "admin",
        "email": "admin@crmditual.com",
        "password": "admin102030",
        "full_name": "Administrador do Sistema",
        "role": UserRole.ADMIN.value,
        "is_active": True
    }
    
    try:
        # Criar sessão do banco de dados
        async with AsyncSessionLocal() as db:
            logger.info("✅ Conexão com banco de dados estabelecida")
            
            # Verificar se usuário admin já existe
            existing_user = await user_service.get_user_by_username(db, admin_data["username"])
            
            if existing_user:
                print(f"⚠️  Usuário '{admin_data['username']}' já existe!")
                print(f"📧 Email: {existing_user.email}")
                print(f"👤 Nome: {existing_user.full_name}")
                print(f"🔑 Role: {existing_user.role.value}")
                print(f"✅ Ativo: {'Sim' if existing_user.is_active else 'Não'}")
                print("\n💡 Se precisar redefinir a senha, delete o usuário primeiro ou use o endpoint de atualização.")
                return
            
            # Verificar se email já está em uso
            existing_email = await user_service.get_user_by_email(db, admin_data["email"])
            if existing_email:
                print(f"⚠️  Email '{admin_data['email']}' já está em uso por outro usuário!")
                print(f"👤 Usuário: {existing_email.username}")
                return
            
            # Criar o usuário admin
            logger.info("🔨 Criando usuário admin...")
            user_create = UserCreate(**admin_data)
            new_user = await user_service.create_user(db, user_create)
            
            if new_user:
                print("🎉 USUÁRIO ADMIN CRIADO COM SUCESSO!")
                print("=" * 50)
                print(f"👤 Username: {new_user.username}")
                print(f"📧 Email: {new_user.email}")
                print(f"🏷️  Nome: {new_user.full_name}")
                print(f"🔑 Role: {new_user.role.value}")
                print(f"🆔 ID: {new_user.id}")
                print(f"📅 Criado em: {new_user.created_at}")
                print("=" * 50)
                print("🔐 CREDENCIAIS DE ACESSO:")
                print(f"   Username: admin")
                print(f"   Password: admin102030")
                print("=" * 50)
                logger.info("✅ Usuário admin criado com sucesso")
            else:
                print("❌ Falha ao criar usuário admin")
                logger.error("Falha ao criar usuário admin")
                
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {str(e)}")
        logger.error(f"Erro ao criar usuário admin: {str(e)}")
        raise


async def test_database_connection():
    """Testar conexão com o banco de dados"""
    try:
        async with AsyncSessionLocal() as db:
            # Tentar fazer uma query simples
            result = await db.execute(text("SELECT 1"))
            if result:
                logger.info("✅ Conexão com banco de dados OK")
                return True
    except Exception as e:
        logger.error(f"❌ Erro de conexão com banco: {e}")
        return False
    
    return False


async def main():
    """Função principal"""
    print("🔧 CRM Ditual - Criador de Usuário Admin")
    print("=" * 50)
    
    # Testar conexão com banco
    print("🔍 Testando conexão com banco de dados...")
    if not await test_database_connection():
        print("❌ Não foi possível conectar ao banco de dados")
        print("💡 Verifique se o PostgreSQL está rodando e acessível")
        sys.exit(1)
    
    # Criar usuário admin
    await create_admin_user()
    
    print("\n✨ Script executado com sucesso!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Script interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        logger.error(f"Erro geral: {e}")
        sys.exit(1)
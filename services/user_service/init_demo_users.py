#!/usr/bin/env python3
"""
Script para inicializar usuários demo no sistema
"""

import asyncio
import sys
import os

# Adicionar o diretório app ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def create_demo_users():
    """Criar usuários demo para o sistema"""
    
    from app.core.database import get_db
    from app.services.user_service import get_user_by_username, create_user
    from app.schemas.user import UserCreate
    from app.models.user import UserRole
    
    print("🔄 Inicializando usuários demo...")
    
    # Configurar conexão com banco
    db_gen = get_db()
    db = await db_gen.__anext__()
    
    try:
        # Definir usuários demo
        demo_users = [
            {
                "username": "admin",
                "email": "admin@crmditual.com",
                "password": "admin123",
                "full_name": "Administrador Sistema",
                "role": UserRole.ADMIN
            },
            {
                "username": "vendedor",
                "email": "vendedor@crmditual.com", 
                "password": "vendedor123",
                "full_name": "João Silva",
                "role": UserRole.VENDAS
            },
            {
                "username": "vendedor2",
                "email": "vendedor2@crmditual.com",
                "password": "vendedor123",
                "full_name": "Maria Santos",
                "role": UserRole.VENDAS
            }
        ]
        
        for user_data in demo_users:
            print(f"🔍 Verificando usuário: {user_data['username']}")
            
            # Verificar se usuário já existe
            existing_user = await get_user_by_username(db, user_data['username'])
            
            if existing_user:
                print(f"✅ Usuário {user_data['username']} já existe")
                continue
            
            # Criar usuário
            user_create = UserCreate(**user_data)
            new_user = await create_user(db, user_create)
            
            print(f"✅ Usuário {user_data['username']} criado com sucesso!")
            print(f"   - Nome: {new_user.full_name}")
            print(f"   - Email: {new_user.email}")
            print(f"   - Role: {new_user.role.value}")
            print(f"   - Ativo: {new_user.is_active}")
        
        print("\n🎉 Inicialização de usuários demo concluída!")
        print("\n📋 Credenciais disponíveis:")
        print("👑 ADMINISTRADOR:")
        print("   Usuário: admin")
        print("   Senha: admin123")
        print("\n👨‍💼 VENDEDORES:")
        print("   Usuário: vendedor")
        print("   Senha: vendedor123")
        print("   ----")
        print("   Usuário: vendedor2") 
        print("   Senha: vendedor123")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários demo: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await db.close()


if __name__ == "__main__":
    try:
        asyncio.run(create_demo_users())
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        sys.exit(1)

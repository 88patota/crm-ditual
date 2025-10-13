#!/usr/bin/env python3
"""
Script para verificar conexão com PostgreSQL
Útil para debug de problemas de autenticação na AWS
"""

import os
import sys
import asyncio
import asyncpg
from datetime import datetime

async def test_connection():
    """Testa conexão com PostgreSQL usando as mesmas configurações dos serviços"""
    
    # Configurações do banco (mesmas do .env.prod)
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'postgres'),
        'port': int(os.getenv('POSTGRES_PORT', '5432')),
        'database': os.getenv('POSTGRES_DB', 'crm_ditual'),
        'user': os.getenv('POSTGRES_USER', 'crm_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'crm_strong_password_2024')
    }
    
    print(f"🔍 Testando conexão PostgreSQL...")
    print(f"📍 Host: {db_config['host']}:{db_config['port']}")
    print(f"🗄️  Database: {db_config['database']}")
    print(f"👤 User: {db_config['user']}")
    print(f"🔐 Password: {'*' * len(db_config['password'])}")
    print(f"⏰ Timestamp: {datetime.now()}")
    print("-" * 50)
    
    try:
        # Tentar conectar
        print("🔄 Tentando conectar...")
        conn = await asyncpg.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        print("✅ Conexão estabelecida com sucesso!")
        
        # Testar uma query simples
        print("🔄 Testando query simples...")
        result = await conn.fetchval('SELECT version()')
        print(f"📊 PostgreSQL Version: {result}")
        
        # Verificar se as tabelas existem
        print("🔄 Verificando tabelas existentes...")
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        if tables:
            print("📋 Tabelas encontradas:")
            for table in tables:
                print(f"   - {table['table_name']}")
        else:
            print("⚠️  Nenhuma tabela encontrada (banco pode estar vazio)")
        
        # Fechar conexão
        await conn.close()
        print("✅ Teste de conexão concluído com sucesso!")
        return True
        
    except asyncpg.InvalidAuthorizationSpecificationError as e:
        print(f"❌ ERRO DE AUTENTICAÇÃO: {e}")
        print("💡 Possíveis causas:")
        print("   - Senha incorreta")
        print("   - Usuário não existe")
        print("   - Configuração pg_hba.conf restritiva")
        return False
        
    except asyncpg.InvalidCatalogNameError as e:
        print(f"❌ ERRO DE BANCO: {e}")
        print("💡 Possíveis causas:")
        print("   - Database não existe")
        print("   - Nome do banco incorreto")
        return False
        
    except asyncpg.CannotConnectNowError as e:
        print(f"❌ ERRO DE CONEXÃO: {e}")
        print("💡 Possíveis causas:")
        print("   - PostgreSQL ainda não está pronto")
        print("   - Muitas conexões simultâneas")
        return False
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")
        return False

def print_env_info():
    """Mostra informações das variáveis de ambiente"""
    print("🌍 Variáveis de ambiente:")
    env_vars = ['POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    
    for var in env_vars:
        value = os.getenv(var, 'NÃO DEFINIDA')
        if 'PASSWORD' in var and value != 'NÃO DEFINIDA':
            value = '*' * len(value)
        print(f"   {var}: {value}")
    print("-" * 50)

async def main():
    """Função principal"""
    print("🚀 Script de Verificação de Conexão PostgreSQL")
    print("=" * 50)
    
    print_env_info()
    
    success = await test_connection()
    
    if success:
        print("\n🎉 Conexão funcionando corretamente!")
        sys.exit(0)
    else:
        print("\n💥 Falha na conexão!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
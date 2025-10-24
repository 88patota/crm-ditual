#!/usr/bin/env python3
"""
Script para resolver conflitos de migração entre user_service e budget_service
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_db_connection():
    """Conecta ao banco de dados PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'crm_ditual'),
        port=os.getenv('POSTGRES_PORT', '5432'),
    )

def clean_alembic_version_table():
    """Limpa completamente a tabela alembic_version"""
    print("🔧 Limpando tabela alembic_version...")
    
    conn = get_db_connection()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    try:
        # Verifica estado atual
        cursor.execute("SELECT version_num FROM alembic_version;")
        versions = cursor.fetchall()
        print(f"📊 Versões encontradas: {[v[0] for v in versions]}")
        
        # Limpa todas as versões
        cursor.execute("DELETE FROM alembic_version;")
        print("✅ Tabela alembic_version limpa!")
        
        # Verifica se está vazia
        cursor.execute("SELECT COUNT(*) FROM alembic_version;")
        count = cursor.fetchone()[0]
        print(f"📊 Registros restantes: {count}")
        
    except Exception as e:
        print(f"❌ Erro ao limpar tabela: {e}")
    finally:
        cursor.close()
        conn.close()

def check_existing_tables():
    """Verifica quais tabelas já existem no banco"""
    print("🔍 Verificando tabelas existentes...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📊 Tabelas encontradas: {tables}")
        
        # Verifica tabelas específicas
        user_tables = [t for t in tables if 'user' in t.lower()]
        budget_tables = [t for t in tables if 'budget' in t.lower()]
        
        print(f"👥 Tabelas do user_service: {user_tables}")
        print(f"💰 Tabelas do budget_service: {budget_tables}")
        
        return {
            'all_tables': tables,
            'user_tables': user_tables,
            'budget_tables': budget_tables,
            'has_users': 'users' in tables,
            'has_budget_items': 'budget_items' in tables
        }
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()

def check_enum_types():
    """Verifica tipos ENUM existentes"""
    print("🔍 Verificando tipos ENUM...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT typname 
            FROM pg_type 
            WHERE typtype = 'e'
            ORDER BY typname;
        """)
        
        enums = [row[0] for row in cursor.fetchall()]
        print(f"📊 ENUMs encontrados: {enums}")
        
        return enums
        
    except Exception as e:
        print(f"❌ Erro ao verificar ENUMs: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def main():
    print("🚀 Iniciando diagnóstico e correção de migrações...")
    print("=" * 60)
    
    # 1. Verifica estado atual
    table_info = check_existing_tables()
    enum_info = check_enum_types()
    
    # 2. Limpa tabela alembic_version
    clean_alembic_version_table()
    
    print("\n" + "=" * 60)
    print("✅ Diagnóstico concluído!")
    print("\n📋 Próximos passos recomendados:")
    
    if table_info.get('has_users') and 'userrole' in enum_info:
        print("1. ⚠️  Tabelas do user_service já existem")
        print("   Execute: docker-compose -f docker-compose.prod.yml exec user_service alembic stamp head")
    else:
        print("1. 👥 Execute migrações do user_service:")
        print("   docker-compose -f docker-compose.prod.yml exec user_service alembic upgrade head")
    
    if table_info.get('has_budget_items'):
        print("2. ⚠️  Tabelas do budget_service já existem")
        print("   Execute: docker-compose -f docker-compose.prod.yml exec budget_service alembic stamp head")
    else:
        print("2. 💰 Execute migrações do budget_service:")
        print("   docker-compose -f docker-compose.prod.yml exec budget_service alembic upgrade head")
    
    print("\n🔚 Script finalizado!")

if __name__ == "__main__":
    main()
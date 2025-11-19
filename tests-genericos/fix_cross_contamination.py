#!/usr/bin/env python3
"""
Script definitivo para resolver contaminação cruzada entre user_service e budget_service
Usa abordagem de stamp base + upgrade head para cada serviço independentemente
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Conecta ao banco de dados usando as variáveis de ambiente."""
    try:
        connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'postgres'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            database=os.getenv('POSTGRES_DB', 'crm_ditual'),
            user=os.getenv('POSTGRES_USER', 'crm_user'),
            password=os.getenv('POSTGRES_PASSWORD', 'crm_strong_password_2024')
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def clean_alembic_version():
    """Limpa completamente a tabela alembic_version"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("🧹 Limpando tabela alembic_version...")
        cursor.execute("DELETE FROM alembic_version;")
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM alembic_version;")
        count = cursor.fetchone()[0]
        print(f"✅ Tabela alembic_version limpa! Registros restantes: {count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar alembic_version: {e}")
        return False

def check_existing_tables():
    """Verifica quais tabelas já existem no banco"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return tables
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return []

def main():
    print("🚀 Iniciando correção definitiva de contaminação cruzada...")
    print("=" * 70)
    
    # 1. Verificar tabelas existentes
    print("🔍 Verificando tabelas existentes...")
    tables = check_existing_tables()
    print(f"📊 Tabelas encontradas: {tables}")
    
    user_tables = [t for t in tables if t in ['users', 'alembic_version']]
    budget_tables = [t for t in tables if t in ['budgets', 'budget_items', 'alembic_version']]
    
    print(f"👥 Tabelas do user_service: {[t for t in user_tables if t != 'alembic_version']}")
    print(f"💰 Tabelas do budget_service: {[t for t in budget_tables if t != 'alembic_version']}")
    
    # 2. Limpar tabela alembic_version
    if not clean_alembic_version():
        print("❌ Falha ao limpar alembic_version. Abortando.")
        return
    
    print("\n" + "=" * 70)
    print("✅ Preparação concluída!")
    print("\n🎯 SOLUÇÃO DEFINITIVA - Execute na ordem EXATA:")
    
    print("\n1️⃣ USER SERVICE:")
    print("   # Stampar como base (vazio)")
    print("   docker-compose -f docker-compose.prod.yml exec user_service alembic stamp base")
    print("   # Fazer upgrade para head (aplicar todas as migrações)")
    print("   docker-compose -f docker-compose.prod.yml exec user_service alembic upgrade head")
    
    print("\n2️⃣ BUDGET SERVICE:")
    print("   # Stampar como base (vazio)")
    print("   docker-compose -f docker-compose.prod.yml exec budget_service alembic stamp base")
    print("   # Fazer upgrade para head (aplicar todas as migrações)")
    print("   docker-compose -f docker-compose.prod.yml exec budget_service alembic upgrade head")
    
    print("\n3️⃣ VERIFICAÇÃO:")
    print("   docker-compose -f docker-compose.prod.yml exec user_service alembic current")
    print("   docker-compose -f docker-compose.prod.yml exec budget_service alembic current")
    
    print("\n💡 COMO FUNCIONA:")
    print("   ✅ stamp base = marca como se nenhuma migração foi aplicada")
    print("   ✅ upgrade head = aplica todas as migrações do zero até a mais recente")
    print("   ✅ Cada serviço usa apenas suas próprias migrações")
    print("   ✅ Não há mais referências cruzadas")
    
    print("\n🔚 Script finalizado!")

if __name__ == "__main__":
    main()
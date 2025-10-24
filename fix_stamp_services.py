#!/usr/bin/env python3
"""
Script para stampar cada serviço com sua própria revisão mais recente
Resolve o problema de referências cruzadas entre user_service e budget_service
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Conecta ao banco de dados PostgreSQL"""
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        database=os.getenv('POSTGRES_DB', 'crm_ditual'),
        port=os.getenv('POSTGRES_PORT', '5432'),
    )

def get_latest_revisions():
    """Obtém as revisões mais recentes de cada serviço"""
    
    # Revisões conhecidas baseadas na estrutura do projeto
    user_service_revisions = [
        '23b3c1dada96',  # Initial migration - create users table
    ]
    
    budget_service_revisions = [
        '001',  # Initial migration - create budgets and budget_items
    ]
    
    return {
        'user_service': user_service_revisions[-1],  # Mais recente
        'budget_service': budget_service_revisions[-1]  # Mais recente
    }

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

def main():
    print("🚀 Iniciando correção de stamp dos serviços...")
    print("=" * 60)
    
    # 1. Limpar tabela alembic_version
    if not clean_alembic_version():
        print("❌ Falha ao limpar alembic_version. Abortando.")
        return
    
    # 2. Obter revisões mais recentes
    revisions = get_latest_revisions()
    print(f"📋 Revisões identificadas:")
    print(f"   👥 user_service: {revisions['user_service']}")
    print(f"   💰 budget_service: {revisions['budget_service']}")
    
    print("\n" + "=" * 60)
    print("✅ Preparação concluída!")
    print("\n📋 Próximos passos OBRIGATÓRIOS:")
    print("1. 👥 Para user_service:")
    print(f"   docker-compose -f docker-compose.prod.yml exec user_service alembic stamp {revisions['user_service']}")
    print("\n2. 💰 Para budget_service:")
    print(f"   docker-compose -f docker-compose.prod.yml exec budget_service alembic stamp {revisions['budget_service']}")
    print("\n3. ✅ Verificar estado:")
    print("   docker-compose -f docker-compose.prod.yml exec user_service alembic current")
    print("   docker-compose -f docker-compose.prod.yml exec budget_service alembic current")
    
    print("\n🔚 Script finalizado!")

if __name__ == "__main__":
    main()
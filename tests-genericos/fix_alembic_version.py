#!/usr/bin/env python3
"""
Script para corrigir o problema de referência cruzada na tabela alembic_version
do budget_service que está tentando localizar uma revisão do user_service.
"""

import os
import psycopg2
from psycopg2 import sql
import sys

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

def check_alembic_version_table(connection):
    """Verifica o conteúdo atual da tabela alembic_version."""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM alembic_version;")
        rows = cursor.fetchall()
        
        print("=== Estado atual da tabela alembic_version ===")
        if rows:
            for row in rows:
                print(f"Revisão encontrada: {row[0]}")
        else:
            print("Tabela alembic_version está vazia")
        
        cursor.close()
        return rows
    except Exception as e:
        print(f"Erro ao verificar tabela alembic_version: {e}")
        return None

def clean_alembic_version_table(connection):
    """Limpa completamente a tabela alembic_version."""
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM alembic_version;")
        connection.commit()
        
        print("✅ Tabela alembic_version limpa com sucesso!")
        
        # Verificar se está realmente vazia
        cursor.execute("SELECT COUNT(*) FROM alembic_version;")
        count = cursor.fetchone()[0]
        print(f"Registros restantes na tabela: {count}")
        
        cursor.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao limpar tabela alembic_version: {e}")
        connection.rollback()
        return False

def main():
    print("🔧 Iniciando correção da tabela alembic_version...")
    
    # Conectar ao banco
    connection = get_db_connection()
    if not connection:
        print("❌ Não foi possível conectar ao banco de dados")
        sys.exit(1)
    
    try:
        # Verificar estado atual
        print("\n1. Verificando estado atual...")
        rows = check_alembic_version_table(connection)
        
        if rows:
            print(f"\n⚠️  Encontradas {len(rows)} revisões na tabela")
            
            # Verificar se há referência incorreta ao user_service
            user_service_revision = '23b3c1dada96'
            has_incorrect_ref = any(user_service_revision in str(row) for row in rows)
            
            if has_incorrect_ref:
                print(f"❌ Encontrada referência incorreta ao user_service: {user_service_revision}")
                
                # Confirmar limpeza
                print("\n2. Limpando tabela alembic_version...")
                if clean_alembic_version_table(connection):
                    print("✅ Correção concluída com sucesso!")
                    print("\nPróximos passos:")
                    print("1. Execute: alembic stamp base")
                    print("2. Execute: alembic upgrade head")
                else:
                    print("❌ Falha na correção")
                    sys.exit(1)
            else:
                print("✅ Não foram encontradas referências incorretas")
        else:
            print("✅ Tabela alembic_version já está vazia")
    
    finally:
        connection.close()
        print("\n🔚 Conexão com banco de dados fechada")

if __name__ == "__main__":
    main()
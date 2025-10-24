#!/usr/bin/env python3
"""
Script para limpar a tabela alembic_version
Parte da refatoração completa das migrações
"""

import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('.env.prod')

def connect_to_db():
    """Conecta ao banco de dados PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="crm_ditual",
            user="crm_user",
            password=os.getenv('POSTGRES_PASSWORD', 'crm_password')
        )
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def clean_alembic_version():
    """Limpa a tabela alembic_version"""
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'alembic_version'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            # Mostrar conteúdo atual
            cursor.execute("SELECT * FROM alembic_version;")
            current_versions = cursor.fetchall()
            
            if current_versions:
                print("🔍 VERSÕES ATUAIS NA TABELA alembic_version:")
                for version in current_versions:
                    print(f"   - {version[0]}")
                
                # Limpar a tabela
                cursor.execute("DELETE FROM alembic_version;")
                conn.commit()
                print("✅ Tabela alembic_version limpa com sucesso!")
            else:
                print("ℹ️  Tabela alembic_version já está vazia")
        else:
            print("ℹ️  Tabela alembic_version não existe")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar tabela alembic_version: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("🧹 LIMPANDO TABELA alembic_version...")
    success = clean_alembic_version()
    
    if success:
        print("🎯 LIMPEZA CONCLUÍDA!")
    else:
        print("❌ FALHA NA LIMPEZA!")
        exit(1)
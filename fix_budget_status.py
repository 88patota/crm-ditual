#!/usr/bin/env python3
"""
Script para corrigir o problema do enum budgetstatus no banco
"""

import psycopg2
import sys

def fix_budget_status_column():
    """Corrige a coluna status da tabela budgets"""
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            database="crm_db",
            user="crm_user",
            password="crm_password"
        )
        
        cursor = conn.cursor()
        
        print("1. Verificando estrutura atual...")
        
        # Verificar se o enum existe
        cursor.execute("SELECT typname FROM pg_type WHERE typname = 'budgetstatus';")
        enum_exists = cursor.fetchone()
        print(f"   Enum budgetstatus existe: {bool(enum_exists)}")
        
        # Verificar estrutura da coluna status
        cursor.execute("""
            SELECT column_name, data_type, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'budgets' AND column_name = 'status';
        """)
        column_info = cursor.fetchone()
        print(f"   Coluna status: {column_info}")
        
        print("\n2. Aplicando correção...")
        
        # Se o enum existe, vamos dropar e recriar a coluna como string
        if enum_exists:
            print("   Dropando constraint da coluna status...")
            cursor.execute("ALTER TABLE budgets ALTER COLUMN status DROP DEFAULT;")
            
            print("   Convertendo coluna para VARCHAR...")
            cursor.execute("ALTER TABLE budgets ALTER COLUMN status TYPE VARCHAR(20);")
            
            print("   Definindo novo default...")
            cursor.execute("ALTER TABLE budgets ALTER COLUMN status SET DEFAULT 'draft';")
            
            print("   Dropando enum...")
            cursor.execute("DROP TYPE IF EXISTS budgetstatus CASCADE;")
        
        # Verificar valores na coluna
        cursor.execute("SELECT DISTINCT status FROM budgets;")
        statuses = cursor.fetchall()
        print(f"   Status existentes na tabela: {[s[0] for s in statuses]}")
        
        # Garantir que todos os status são válidos
        print("   Atualizando status inválidos para 'draft'...")
        cursor.execute("""
            UPDATE budgets 
            SET status = 'draft' 
            WHERE status IS NULL 
               OR status NOT IN ('draft', 'pending', 'approved', 'rejected', 'expired');
        """)
        
        affected = cursor.rowcount
        print(f"   {affected} registros atualizados")
        
        # Commit das mudanças
        conn.commit()
        print("\n3. Correção aplicada com sucesso!")
        
        # Verificar resultado final
        cursor.execute("""
            SELECT column_name, data_type, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'budgets' AND column_name = 'status';
        """)
        final_column = cursor.fetchone()
        print(f"   Estrutura final: {final_column}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erro ao corrigir: {e}")
        return False

if __name__ == "__main__":
    success = fix_budget_status_column()
    sys.exit(0 if success else 1)

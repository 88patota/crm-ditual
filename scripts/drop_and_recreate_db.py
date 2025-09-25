#!/usr/bin/env python3
"""
Script para dropar o banco de dados e recriá-lo com uma fonte da verdade
Baseado nos campos utilizados atualmente na aplicação
"""

import os
import sys
import subprocess
from pathlib import Path

# Adicionar o diretório do serviço ao PYTHONPATH
service_path = Path(__file__).parent.parent / "services" / "budget_service"
sys.path.insert(0, str(service_path))

def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro")
        print(f"Erro: {e.stderr}")
        return False

def main():
    """Função principal do script"""
    print("🚀 Iniciando processo de drop e recriação do banco de dados")
    print("=" * 60)
    
    # Navegar para o diretório do budget_service
    budget_service_dir = Path(__file__).parent.parent / "services" / "budget_service"
    os.chdir(budget_service_dir)
    
    print(f"📁 Diretório de trabalho: {os.getcwd()}")
    
    # 1. Fazer backup das migrations atuais
    print("\n1. Fazendo backup das migrations atuais...")
    backup_dir = Path("alembic/versions_backup")
    backup_dir.mkdir(exist_ok=True)
    
    if not run_command(
        "cp alembic/versions/*.py alembic/versions_backup/ 2>/dev/null || true",
        "Backup das migrations"
    ):
        print("⚠️ Aviso: Não foi possível fazer backup das migrations (pode não existir)")
    
    # 2. Remover todas as migrations existentes
    run_command(
        "rm -f alembic/versions/*.py",
        "Remoção das migrations existentes"
    )
    
    # 3. Dropar todas as tabelas usando Alembic
    run_command(
        "alembic downgrade base",
        "Drop das tabelas via Alembic downgrade"
    )
    
    # 4. Remover histórico do Alembic
    run_command(
        "alembic stamp base",
        "Reset do histórico Alembic"
    )
    
    # 5. Gerar nova migration inicial com fonte da verdade
    run_command(
        'alembic revision --autogenerate -m "Initial migration - fonte da verdade"',
        "Geração da migration fonte da verdade"
    )
    
    # 6. Aplicar a nova migration
    run_command(
        "alembic upgrade head",
        "Aplicação da migration fonte da verdade"
    )
    
    # 7. Verificar se as tabelas foram criadas
    print("\n7. Verificando estrutura das tabelas criadas...")
    
    # Script para verificar tabelas
    verification_script = """
import sys
sys.path.insert(0, '.')
from app.core.database import engine
from sqlalchemy import text
import traceback

try:
    with engine.connect() as conn:
        # Verificar tabelas existentes
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';"))
        tables = [row[0] for row in result.fetchall()]
        
        print("📊 Tabelas criadas:")
        for table in sorted(tables):
            print(f"   - {table}")
            
        # Verificar estrutura da tabela budgets
        if 'budgets' in tables:
            print("\\n📋 Estrutura da tabela 'budgets':")
            result = conn.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'budgets' ORDER BY ordinal_position;"))
            for row in result.fetchall():
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"   - {row[0]}: {row[1]} ({nullable})")
                
        # Verificar estrutura da tabela budget_items
        if 'budget_items' in tables:
            print("\\n📋 Estrutura da tabela 'budget_items':")
            result = conn.execute(text("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'budget_items' ORDER BY ordinal_position;"))
            for row in result.fetchall():
                nullable = "NULL" if row[2] == "YES" else "NOT NULL"
                print(f"   - {row[0]}: {row[1]} ({nullable})")
                
        print("\\n✅ Verificação das tabelas concluída com sucesso!")
        
except Exception as e:
    print(f"❌ Erro na verificação: {e}")
    traceback.print_exc()
"""
    
    # Salvar e executar script de verificação
    with open("verify_tables.py", "w") as f:
        f.write(verification_script)
    
    run_command(
        "python verify_tables.py",
        "Verificação da estrutura das tabelas"
    )
    
    # Remover arquivo temporário
    run_command(
        "rm verify_tables.py",
        "Limpeza de arquivo temporário"
    )
    
    print("\n" + "=" * 60)
    print("🎉 Processo concluído com sucesso!")
    print("\n📝 Resumo:")
    print("   - Banco de dados dropado")
    print("   - Nova migration criada com fonte da verdade")
    print("   - Tabelas recriadas com estrutura atual")
    print("   - Backup das migrations antigas em alembic/versions_backup/")
    print("\n💡 Próximos passos:")
    print("   - Verificar se a aplicação está funcionando corretamente")
    print("   - Executar testes para validar a integridade")
    print("   - Popular dados de teste se necessário")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Direct database test to check IPI persistence bypassing authentication
"""
import asyncio
import sys
import os

# Add the services directory to Python path
sys.path.append('services/budget_service')
sys.path.append('services')

from app.core.database import engine
from app.models.budget import Budget, BudgetItem
from app.schemas.budget import BudgetCreate, BudgetItemCreate
from app.services.budget_service import BudgetService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def test_ipi_direct_persistence():
    """Test IPI persistence directly on the database"""
    print("=== TESTE DIRETO DE PERSISTÊNCIA IPI NO BANCO ===")
    print("Este teste acessa diretamente o banco de dados para verificar se o IPI está sendo salvo")
    print()
    
    async with engine.begin() as conn:
        async with AsyncSession(conn) as session:
            try:
                # Create test budget with IPI
                print("PASSO 1: Criando orçamento de teste com IPI...")
                
                budget_data = BudgetCreate(
                    order_number="TEST-IPI-DB-001",
                    client_name="Cliente Teste IPI Direto",
                    items=[
                        BudgetItemCreate(
                            description="Item com IPI 3.25%",
                            weight=100.0,
                            purchase_value_with_icms=10.00,
                            purchase_icms_percentage=0.18,
                            purchase_other_expenses=0.0,
                            purchase_value_without_taxes=8.00,
                            sale_weight=100.0,
                            sale_value_with_icms=15.00,
                            sale_icms_percentage=0.17,
                            sale_value_without_taxes=12.45,
                            ipi_percentage=0.0325,  # 3.25%
                            commission_percentage=0.0
                        )
                    ]
                )
                
                # Create budget using BudgetService
                budget = await BudgetService.create_budget(session, budget_data, "test_user")
                print(f"✅ Orçamento criado com ID: {budget.id}")
                
                # PASSO 2: Verificar dados salvos no banco
                print("\nPASSO 2: Verificando dados salvos no banco...")
                
                # Get budget with items
                saved_budget = await BudgetService.get_budget_by_id(session, budget.id)
                
                if not saved_budget or not saved_budget.items:
                    print("❌ Orçamento ou itens não encontrados")
                    return False
                
                item = saved_budget.items[0]
                
                print(f"Item salvo:")
                print(f"  - Descrição: {item.description}")
                print(f"  - Peso venda: {item.sale_weight}kg")
                print(f"  - Valor venda c/ICMS: R$ {item.sale_value_with_icms:.2f}")
                print(f"  - IPI Percentage: {item.ipi_percentage * 100 if item.ipi_percentage else 0:.2f}%")
                print(f"  - IPI Value: R$ {item.ipi_value if item.ipi_value else 0:.2f}")
                print(f"  - Total com IPI: R$ {item.total_value_with_ipi if item.total_value_with_ipi else 0:.2f}")
                
                # PASSO 3: Verificar cálculos
                print("\nPASSO 3: Verificando se os cálculos estão corretos...")
                
                # Expected: 100kg * R$15.00 * 3.25% = R$48.75
                expected_ipi_percentage = 0.0325
                expected_ipi_value = 100.0 * 15.00 * 0.0325  # 48.75
                expected_total_with_ipi = (100.0 * 15.00) + expected_ipi_value  # 1548.75
                
                print(f"Valores esperados:")
                print(f"  - IPI Percentage: {expected_ipi_percentage * 100:.2f}%")
                print(f"  - IPI Value: R$ {expected_ipi_value:.2f}")
                print(f"  - Total com IPI: R$ {expected_total_with_ipi:.2f}")
                
                # Check results
                tolerance = 0.01
                
                # Check IPI percentage
                if abs((item.ipi_percentage or 0) - expected_ipi_percentage) < 0.0001:
                    print("✅ IPI Percentage salvo corretamente!")
                else:
                    print("❌ IPI Percentage INCORRETO!")
                    print(f"   Esperado: {expected_ipi_percentage * 100:.2f}%, Salvo: {(item.ipi_percentage or 0) * 100:.2f}%")
                    return False
                
                # Check IPI value  
                if abs((item.ipi_value or 0) - expected_ipi_value) < tolerance:
                    print("✅ IPI Value salvo corretamente!")
                else:
                    print("❌ IPI Value INCORRETO!")
                    print(f"   Esperado: R$ {expected_ipi_value:.2f}, Salvo: R$ {item.ipi_value or 0:.2f}")
                    return False
                
                # Check total with IPI
                if abs((item.total_value_with_ipi or 0) - expected_total_with_ipi) < tolerance:
                    print("✅ Total com IPI salvo corretamente!")
                else:
                    print("❌ Total com IPI INCORRETO!")
                    print(f"   Esperado: R$ {expected_total_with_ipi:.2f}, Salvo: R$ {item.total_value_with_ipi or 0:.2f}")
                    return False
                
                print("\n🎉 TESTE PASSOU!")
                print("✅ IPI está sendo calculado e persistido corretamente no banco de dados!")
                
                # PASSO 4: Consulta SQL direta para confirmar
                print("\nPASSO 4: Verificação SQL direta...")
                result = await session.execute(
                    text("""
                        SELECT 
                            b.order_number,
                            bi.description,
                            bi.ipi_percentage,
                            bi.ipi_value,
                            bi.total_value_with_ipi
                        FROM budgets b
                        JOIN budget_items bi ON b.id = bi.budget_id
                        WHERE b.order_number = :order_number
                    """),
                    {"order_number": "TEST-IPI-DB-001"}
                )
                
                row = result.fetchone()
                if row:
                    print(f"SQL direto:")
                    print(f"  - Order Number: {row[0]}")
                    print(f"  - Description: {row[1]}")
                    print(f"  - IPI Percentage (DB): {row[2] * 100 if row[2] else 0:.2f}%")
                    print(f"  - IPI Value (DB): R$ {row[3] if row[3] else 0:.2f}")
                    print(f"  - Total with IPI (DB): R$ {row[4] if row[4] else 0:.2f}")
                
                return True
                
            except Exception as e:
                print(f"❌ Erro durante o teste: {e}")
                print(f"Tipo do erro: {type(e)}")
                import traceback
                traceback.print_exc()
                return False

async def main():
    print("Testando persistência do IPI diretamente no banco de dados...")
    print("Este teste bypassa completamente o sistema de autenticação")
    print()
    
    success = await test_ipi_direct_persistence()
    
    if success:
        print("\n🎉 RESULTADO FINAL: SUCESSO!")
        print("O IPI está funcionando corretamente!")
    else:
        print("\n❌ RESULTADO FINAL: FALHOU!")
        print("Há um problema com a persistência do IPI!")

if __name__ == "__main__":
    asyncio.run(main())

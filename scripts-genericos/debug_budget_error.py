#!/usr/bin/env python3

import sys
import os
sys.path.append('services/budget_service')

def test_budget_creation():
    """Testa criação de orçamento simplificado para identificar o erro"""
    
    try:
        print("1. Importando módulos...")
        from app.schemas.budget import BudgetSimplifiedCreate, BudgetItemSimplified, BudgetItemCreate, BudgetCreate
        from app.services.budget_calculator import BudgetCalculatorService
        print("✅ Importações OK")

        # Dados exatos da requisição que está falhando
        test_data = {
            "order_number": "PED-0001",
            "client_name": "Cliente Teste",
            "status": "draft",
            "items": [{
                "description": "item",
                "peso_compra": 10,
                "peso_venda": 10,
                "valor_com_icms_compra": 33.11,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0,
                "valor_com_icms_venda": 87.12,
                "percentual_icms_venda": 0.18
            }]
        }

        print("2. Testando validação do schema...")
        budget_simplified = BudgetSimplifiedCreate(**test_data)
        print("✅ Schema validation passou")

        print("3. Testando validação dos dados...")
        budget_dict = budget_simplified.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            print("❌ Erros de validação:", errors)
            return False
        print("✅ Validação dos dados passou")

        print("4. Testando cálculo simplificado...")
        calculation_result = BudgetCalculatorService.calculate_simplified_budget(budget_simplified.items)
        print("✅ Cálculo simplificado passou")
        
        print("5. Resultado do cálculo:")
        print("   Totais:", calculation_result['totals'])
        print("   Número de itens:", len(calculation_result['items']))
        
        print("6. Testando conversão para BudgetCreate...")
        # Simular o que acontece no endpoint
        complete_budget_data = BudgetCreate(
            order_number=budget_simplified.order_number or "PED-TEST",
            client_name=budget_simplified.client_name,
            markup_percentage=calculation_result['totals']['markup_percentage'],
            notes=budget_simplified.notes,
            expires_at=budget_simplified.expires_at,
            items=[BudgetItemCreate(**item_data) for item_data in calculation_result['items']]
        )
        print("✅ Conversão para BudgetCreate passou")
        
        print("7. Verificando campos dos itens convertidos...")
        for i, item in enumerate(complete_budget_data.items):
            print(f"   Item {i+1}:")
            print(f"     description: {item.description}")
            print(f"     purchase_value_without_taxes: {item.purchase_value_without_taxes}")
            print(f"     sale_value_without_taxes: {item.sale_value_without_taxes}")
            print(f"     weight: {item.weight}")
            print(f"     sale_weight: {item.sale_weight}")
        
        return True

    except Exception as e:
        print(f"❌ Erro encontrado: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== DEBUG BUDGET ERROR ===")
    success = test_budget_creation()
    if success:
        print("\n✅ Teste concluído com sucesso - problema pode estar na criação do banco")
    else:
        print("\n❌ Problema identificado no processamento")

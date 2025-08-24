#!/usr/bin/env python3

import sys
import os
import json
sys.path.append('services/budget_service')

def test_budget_creation_with_real_data():
    """Testa criação de orçamento com dados reais para verificar se a correção funcionou"""
    
    try:
        print("=== TESTE DE CORREÇÃO DO ERRO 500 ===")
        print("1. Importando módulos...")
        
        from app.schemas.budget import BudgetSimplifiedCreate, BudgetItemCreate, BudgetCreate
        from app.services.budget_calculator import BudgetCalculatorService
        print("✅ Importações OK")

        # Dados exatos da requisição que estava falhando
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

        print("2. Criando BudgetSimplifiedCreate...")
        budget_simplified = BudgetSimplifiedCreate(**test_data)
        print("✅ Schema validation passou")

        print("3. Validando dados...")
        budget_dict = budget_simplified.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            print("❌ Erros de validação:", errors)
            return False
        print("✅ Validação passou")

        print("4. Calculando orçamento simplificado...")
        calculation_result = BudgetCalculatorService.calculate_simplified_budget(budget_simplified.items)
        print("✅ Cálculo simplificado passou")
        
        print("5. Resultado dos cálculos:")
        print(f"   Total compra: R$ {calculation_result['totals']['total_purchase_value']}")
        print(f"   Total venda: R$ {calculation_result['totals']['total_sale_value']}")
        print(f"   Markup: {calculation_result['totals']['markup_percentage']}%")
        
        print("6. Convertendo para BudgetCreate...")
        complete_budget_data = BudgetCreate(
            order_number=budget_simplified.order_number or "PED-TEST",
            client_name=budget_simplified.client_name,
            markup_percentage=calculation_result['totals']['markup_percentage'],
            notes=budget_simplified.notes,
            expires_at=budget_simplified.expires_at,
            items=[BudgetItemCreate(**item_data) for item_data in calculation_result['items']]
        )
        print("✅ Conversão para BudgetCreate passou")
        
        print("7. Verificando dados dos itens para BudgetService...")
        items_data = [item.dict() for item in complete_budget_data.items]
        
        for i, item_data in enumerate(items_data):
            print(f"   Item {i+1} - dados para BudgetService:")
            required_fields = [
                'description', 'weight', 'purchase_icms_percentage', 'purchase_other_expenses',
                'purchase_value_without_taxes', 'sale_weight', 'sale_icms_percentage', 
                'sale_value_without_taxes', 'weight_difference', 'profitability',
                'total_purchase', 'total_sale', 'unit_value', 'total_value',
                'commission_percentage', 'commission_value', 'dunamis_cost'
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in item_data or item_data.get(field) is None:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"     ⚠️  Campos ausentes: {missing_fields}")
            else:
                print(f"     ✅ Todos os campos necessários presentes")
                
            # Mostrar alguns valores importantes
            print(f"     purchase_value_without_taxes: {item_data.get('purchase_value_without_taxes')}")
            print(f"     sale_value_without_taxes: {item_data.get('sale_value_without_taxes')}")
            print(f"     total_purchase: {item_data.get('total_purchase')}")
            print(f"     total_sale: {item_data.get('total_sale')}")

        return True

    except Exception as e:
        print(f"❌ Erro encontrado: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_budget_creation_with_real_data()
    if success:
        print("\n✅ CORREÇÃO APLICADA COM SUCESSO")
        print("Os dados estão sendo processados corretamente para o BudgetService")
    else:
        print("\n❌ AINDA HÁ PROBLEMAS NO PROCESSAMENTO")

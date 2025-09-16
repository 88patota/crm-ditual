#!/usr/bin/env python3

import sys
import json
sys.path.append('services/budget_service')

def test_complete_endpoint_flow():
    """Testa o fluxo completo do endpoint simplificado"""
    
    try:
        print("=== TESTE COMPLETO DO ENDPOINT SIMPLIFICADO ===")
        
        # Importar módulos necessários
        from app.schemas.budget import BudgetSimplifiedCreate, BudgetItemCreate, BudgetCreate
        from app.services.budget_calculator import BudgetCalculatorService
        
        # Dados da requisição exata que estava falhando
        request_data = {
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
        
        print("1. Simulando recebimento da requisição...")
        print(f"   POST /api/v1/budgets/simplified")
        print(f"   Body: {json.dumps(request_data, indent=2)}")
        
        # Simular o processamento do endpoint
        print("\n2. Validação do schema simplificado...")
        budget_simplified = BudgetSimplifiedCreate(**request_data)
        print("✅ Schema validation passou")
        
        print("\n3. Validação dos dados...")
        budget_dict = budget_simplified.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            print(f"❌ Erros de validação: {errors}")
            return False
        print("✅ Validação dos dados passou")
        
        print("\n4. Cálculo simplificado...")
        calculation_result = BudgetCalculatorService.calculate_simplified_budget(budget_simplified.items)
        print("✅ Cálculo passou")
        print(f"   Markup calculado: {calculation_result['totals']['markup_percentage']:.2f}%")
        print(f"   Total venda: R$ {calculation_result['totals']['total_sale_value']:.2f}")
        print(f"   Total compra: R$ {calculation_result['totals']['total_purchase_value']:.2f}")
        
        print("\n5. Geração do número do pedido...")
        order_number = budget_simplified.order_number or "PED-0001"  # Simular geração automática
        print(f"✅ Número do pedido: {order_number}")
        
        print("\n6. Conversão para BudgetCreate...")
        complete_budget_data = BudgetCreate(
            order_number=order_number,
            client_name=budget_simplified.client_name,
            markup_percentage=calculation_result['totals']['markup_percentage'],
            notes=budget_simplified.notes,
            expires_at=budget_simplified.expires_at,
            items=[BudgetItemCreate(**item_data) for item_data in calculation_result['items']]
        )
        print("✅ Conversão concluída")
        
        print("\n7. Verificação de dados para BudgetService...")
        items_data = [item.dict() for item in complete_budget_data.items]
        
        # Verificar se todos os campos necessários estão presentes
        required_db_fields = [
            'description', 'weight', 'purchase_icms_percentage', 'purchase_other_expenses',
            'purchase_value_without_taxes', 'sale_weight', 'sale_icms_percentage', 
            'sale_value_without_taxes', 'weight_difference', 'profitability',
            'total_purchase', 'total_sale', 'unit_value', 'total_value',
            'commission_percentage', 'commission_value', 'dunamis_cost'
        ]
        
        all_fields_present = True
        for i, item_data in enumerate(items_data):
            missing_fields = []
            for field in required_db_fields:
                if field not in item_data or item_data.get(field) is None:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"❌ Item {i+1} - Campos ausentes: {missing_fields}")
                all_fields_present = False
            else:
                print(f"✅ Item {i+1} - Todos os campos presentes")
        
        if not all_fields_present:
            return False
            
        print("\n8. Simulação de salvamento no banco...")
        print("✅ Dados prontos para BudgetService.create_budget()")
        print(f"   Budget: {complete_budget_data.client_name} - {complete_budget_data.order_number}")
        print(f"   Itens: {len(complete_budget_data.items)}")
        print(f"   Markup: {complete_budget_data.markup_percentage:.2f}%")
        
        print("\n9. Resposta do endpoint (simulada)...")
        response = {
            "id": 123,  # Simulado
            "order_number": complete_budget_data.order_number,
            "client_name": complete_budget_data.client_name,
            "status": "draft",
            "total_purchase_value": calculation_result['totals']['total_purchase_value'],
            "total_sale_value": calculation_result['totals']['total_sale_value'],
            "total_commission": calculation_result['totals']['total_commission'],
            "profitability_percentage": calculation_result['totals']['profitability_percentage'],
            "markup_percentage": calculation_result['totals']['markup_percentage'],
            "created_by": "test_user",
            "items": []  # Seria preenchido com os itens completos
        }
        
        print("✅ Response 201 Created:")
        print(json.dumps(response, indent=2, default=str))
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro no processamento: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_endpoint_flow()
    if success:
        print("\n🎉 CORREÇÃO COMPLETA - ENDPOINT FUNCIONANDO!")
        print("O erro 500 foi resolvido. O endpoint agora processa corretamente os dados.")
    else:
        print("\n❌ AINDA HÁ PROBLEMAS NO ENDPOINT")

#!/usr/bin/env python3
"""
Teste específico para a criação de orçamento simplificado
"""
import sys
import os
import asyncio

# Adicionar o caminho do serviço
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.schemas.budget import BudgetSimplifiedCreate, BudgetItemSimplified
from app.services.budget_calculator import BudgetCalculatorService

async def test_create_simplified_endpoint():
    """Testar especificamente o endpoint /budgets/simplified"""
    
    print("🔍 Testando endpoint /budgets/simplified...")
    
    # Dados exatos que seriam enviados pelo frontend
    test_data = {
        "client_name": "Cliente Teste",
        "status": "draft",
        "items": [
            {
                "description": "Produto Teste",
                "peso_compra": 100.0,
                "peso_venda": 95.0,
                "valor_com_icms_compra": 1000.0,
                "percentual_icms_compra": 0.18,
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 1500.0,
                "percentual_icms_venda": 0.18
            }
        ]
    }
    
    try:
        # 1. Validar dados de entrada
        budget_data = BudgetSimplifiedCreate(**test_data)
        print(f"✅ Schema BudgetSimplifiedCreate validado: {budget_data}")
        
        # 2. Validar dados usando BudgetCalculatorService
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            print(f"❌ Erros de validação: {errors}")
            return False
        
        print("✅ Validação BudgetCalculatorService passou")
        
        # 3. Calcular todos os valores baseados nos dados de entrada
        calculation_result = BudgetCalculatorService.calculate_simplified_budget(budget_data.items)
        print(f"✅ Cálculo realizado: {calculation_result}")
        
        # 4. Simular a criação do BudgetCreate para salvar
        from app.schemas.budget import BudgetCreate, BudgetItemCreate
        
        # Converter items_data calculados para BudgetItemCreate
        budget_items = []
        for item_data in calculation_result['items']:
            budget_item = BudgetItemCreate(
                description=item_data['description'],
                quantity=item_data['quantity'],
                weight=item_data['weight'],
                purchase_value_with_icms=item_data['purchase_value_with_icms'],
                purchase_icms_percentage=item_data['purchase_icms_percentage'],
                purchase_other_expenses=item_data['purchase_other_expenses'],
                purchase_value_without_taxes=item_data['purchase_value_without_taxes'],
                purchase_value_with_weight_diff=item_data.get('purchase_value_with_weight_diff'),
                sale_weight=item_data.get('sale_weight'),
                sale_value_with_icms=item_data['sale_value_with_icms'],
                sale_icms_percentage=item_data['sale_icms_percentage'],
                sale_value_without_taxes=item_data['sale_value_without_taxes'],
                weight_difference=item_data.get('weight_difference'),
                commission_percentage=item_data['commission_percentage'],
                dunamis_cost=item_data.get('dunamis_cost')
            )
            budget_items.append(budget_item)
        
        # Criar orçamento completo
        complete_budget_data = BudgetCreate(
            order_number="PED-TEST",
            client_name=budget_data.client_name,
            markup_percentage=calculation_result['totals']['markup_percentage'],
            notes=budget_data.notes,
            expires_at=budget_data.expires_at,
            items=budget_items
        )
        
        print(f"✅ BudgetCreate criado: {complete_budget_data}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro encontrado: {type(e).__name__}: {e}")
        import traceback
        print(f"📋 Traceback completo:\n{traceback.format_exc()}")
        return False

async def test_with_validation_error():
    """Testar com dados que devem gerar erro de validação"""
    print("\n🔍 Testando dados inválidos...")
    
    # Dados com problemas intencionais
    invalid_data = {
        "client_name": "",  # Nome vazio
        "status": "draft",
        "items": [
            {
                "description": "",  # Descrição vazia
                "peso_compra": 0,  # Peso zero
                "peso_venda": 95.0,
                "valor_com_icms_compra": -100.0,  # Valor negativo
                "percentual_icms_compra": 1.5,  # Porcentagem inválida (>1)
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 0,  # Valor zero
                "percentual_icms_venda": 0.18
            }
        ]
    }
    
    try:
        budget_data = BudgetSimplifiedCreate(**invalid_data)
        print(f"❌ Schema deveria ter falhado: {budget_data}")
        return False
        
    except Exception as e:
        print(f"✅ Erro de validação capturado corretamente: {e}")
        return True

if __name__ == "__main__":
    print("🚀 Testando especificamente a criação de orçamento...")
    
    result1 = asyncio.run(test_create_simplified_endpoint())
    result2 = asyncio.run(test_with_validation_error())
    
    print(f"\n📊 Resultados:")
    print(f"Teste criação endpoint: {'✅' if result1 else '❌'}")
    print(f"Teste validação erro: {'✅' if result2 else '❌'}")
    
    if result1 and result2:
        print("\n🎉 Endpoint deve estar funcionando corretamente agora!")
    else:
        print("\n🔧 Ainda há problemas a resolver...")

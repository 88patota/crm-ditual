#!/usr/bin/env python3
"""
Script para reproduzir e debugar o erro 400 ao criar orçamento
"""
import sys
import os

# Adicionar o caminho do serviço
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.schemas.budget import BudgetSimplifiedCreate, BudgetItemSimplified
from app.services.budget_calculator import BudgetCalculatorService

def test_error_reproduction():
    """Reproduzir o erro 400 com dados similares aos do frontend"""
    
    print("🔍 Testando reprodução do erro 400...")
    
    # Dados similares aos enviados pelo frontend
    test_data = {
        "order_number": "PED-0001",
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
    
    print(f"📤 Dados de teste: {test_data}")
    
    try:
        # Tentar criar schema
        budget_data = BudgetSimplifiedCreate(**test_data)
        print(f"✅ Schema criado com sucesso: {budget_data}")
        
        # Tentar validar dados usando o BudgetCalculatorService
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        
        if errors:
            print(f"❌ Erros na validação: {errors}")
            return False
        else:
            print("✅ Validação passou")
        
        # Tentar calcular orçamento
        calculated = BudgetCalculatorService.calculate_simplified_budget(budget_data.items)
        print(f"✅ Cálculo realizado: {calculated}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro encontrado: {type(e).__name__}: {e}")
        import traceback
        print(f"📋 Traceback completo:\n{traceback.format_exc()}")
        return False

def test_business_rules_calculator():
    """Testar com o BusinessRulesCalculator"""
    try:
        from app.services.business_rules_calculator import BusinessRulesCalculator
        
        print("\n🔍 Testando BusinessRulesCalculator...")
        
        item_data = {
            "description": "Produto Teste", 
            "peso_compra": 100.0,
            "peso_venda": 95.0,
            "valor_com_icms_compra": 1000.0,
            "percentual_icms_compra": 0.18,
            "outras_despesas_item": 0.0,
            "valor_com_icms_venda": 1500.0,
            "percentual_icms_venda": 0.18
        }
        
        print(f"📤 Dados do item: {item_data}")
        
        # Validar item
        errors = BusinessRulesCalculator.validate_item_data(item_data)
        if errors:
            print(f"❌ Erros na validação do BusinessRules: {errors}")
            return False
        
        print("✅ BusinessRulesCalculator validação passou")
        
        # Tentar calcular item
        calculated_item = BusinessRulesCalculator.calculate_complete_item(
            item_data, 0.0, 100.0
        )
        
        print(f"✅ BusinessRulesCalculator cálculo realizado: {calculated_item}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no BusinessRulesCalculator: {type(e).__name__}: {e}")
        import traceback
        print(f"📋 Traceback completo:\n{traceback.format_exc()}")
        return False

def test_api_simulation():
    """Simular o que acontece no endpoint da API"""
    try:
        from app.services.business_rules_calculator import BusinessRulesCalculator
        from app.schemas.budget import BudgetCalculation
        
        print("\n🔍 Simulando endpoint da API...")
        
        # Dados como enviados pelo frontend
        budget_data_raw = {
            "order_number": "PED-0001",
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
        
        # Converter para schema Pydantic
        budget_data = BudgetSimplifiedCreate(**budget_data_raw)
        print(f"✅ Schema Pydantic criado: {budget_data}")
        
        # Converter dados para formato esperado pelo BusinessRulesCalculator
        items_data = []
        total_peso_pedido = 0.0
        
        for item in budget_data.items:
            item_dict = item.dict()
            total_peso_pedido += item_dict.get('peso_compra', 1.0)
            items_data.append(item_dict)
        
        print(f"✅ Items convertidos: {items_data}")
        print(f"✅ Total peso pedido: {total_peso_pedido}")
        
        # Validar dados usando business rules
        for i, item_data in enumerate(items_data):
            errors = BusinessRulesCalculator.validate_item_data(item_data)
            if errors:
                print(f"❌ Erro na validação do item {i+1}: {errors}")
                return False
        
        print("✅ Todos os itens passaram na validação")
        
        # Calcular usando BusinessRulesCalculator
        outras_despesas_totais = 0.0
        
        calculated_items = []
        total_purchase_value = 0.0
        total_sale_value = 0.0
        total_commission = 0.0
        
        for item_data in items_data:
            calculated_item = BusinessRulesCalculator.calculate_complete_item(
                item_data, outras_despesas_totais, total_peso_pedido
            )
            calculated_items.append(calculated_item)
            
            total_purchase_value += calculated_item['total_compra_item']
            total_sale_value += calculated_item['total_venda_item']
            total_commission += calculated_item['valor_comissao']
        
        print(f"✅ Itens calculados: {len(calculated_items)}")
        print(f"✅ Total compra: {total_purchase_value}")
        print(f"✅ Total venda: {total_sale_value}")
        print(f"✅ Total comissão: {total_commission}")
        
        # Calcular markup
        if total_purchase_value > 0:
            markup_percentage = ((total_sale_value - total_purchase_value) / total_purchase_value) * 100
            profitability_percentage = markup_percentage
        else:
            markup_percentage = 0.0
            profitability_percentage = 0.0
        
        print(f"✅ Markup: {markup_percentage}%")
        print(f"✅ Rentabilidade: {profitability_percentage}%")
        
        # Preparar resposta como seria enviada pela API
        items_calculations = []
        for item in calculated_items:
            items_calculations.append({
                'description': item['description'],
                'peso_compra': item['peso_compra'],
                'peso_venda': item['peso_venda'], 
                'total_purchase': item['total_compra_item'],
                'total_sale': item['total_venda_item'],
                'profitability': item['rentabilidade_item'] * 100,
                'commission_value': item['valor_comissao']
            })
        
        calculation_response = BudgetCalculation(
            total_purchase_value=round(total_purchase_value, 2),
            total_sale_value=round(total_sale_value, 2),
            total_commission=round(total_commission, 2),
            profitability_percentage=round(profitability_percentage, 2),
            markup_percentage=round(markup_percentage, 2),
            items_calculations=items_calculations
        )
        
        print(f"✅ Resposta final: {calculation_response}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na simulação da API: {type(e).__name__}: {e}")
        import traceback
        print(f"📋 Traceback completo:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando debug do erro 400...")
    
    result1 = test_error_reproduction()
    result2 = test_business_rules_calculator()
    result3 = test_api_simulation()
    
    print(f"\n📊 Resultados:")
    print(f"Test Error Reproduction: {'✅' if result1 else '❌'}")
    print(f"Business Rules Calculator: {'✅' if result2 else '❌'}")
    print(f"API Simulation: {'✅' if result3 else '❌'}")
    
    if all([result1, result2, result3]):
        print("\n🎉 Todos os testes passaram! O problema pode estar em outro lugar.")
    else:
        print("\n🔧 Encontramos o problema! Vamos investigar mais...")

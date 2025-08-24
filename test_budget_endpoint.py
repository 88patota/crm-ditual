#!/usr/bin/env python3
"""
Teste para verificar se o endpoint /api/v1/budgets/calculate-simplified está funcionando corretamente
"""
import sys
import os
sys.path.append('services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_business_rules_calculator():
    """Testa se o BusinessRulesCalculator está funcionando corretamente"""
    print("Testando BusinessRulesCalculator...")
    
    # Dados de teste similares ao que o frontend enviaria
    sample_items = [
        {
            'description': 'Item de teste',
            'quantity': 1,
            'peso_compra': 10.0,
            'peso_venda': 10.0,
            'valor_com_icms_compra': 100.0,
            'percentual_icms_compra': 0.18,
            'outras_despesas_item': 5.0,
            'valor_com_icms_venda': 150.0,
            'percentual_icms_venda': 0.17
        }
    ]
    
    outras_despesas_totais = 10.0
    
    try:
        # Testar o método que está sendo usado no endpoint
        calculator = BusinessRulesCalculator()
        soma_pesos_pedido = sum(item['peso_compra'] for item in sample_items)
        result = calculator.calculate_complete_budget(sample_items, outras_despesas_totais, soma_pesos_pedido)
        
        print("✓ BusinessRulesCalculator.calculate_complete_budget() executou com sucesso")
        print(f"✓ Total compra: {result['totals']['soma_total_compra']}")
        print(f"✓ Total venda: {result['totals']['soma_total_venda']}")
        print(f"✓ Markup: {result['totals']['markup_pedido']}%")
        print(f"✓ Comissão total: {result['totals']['comissao_total_pedido']}")
        print(f"✓ Número de itens processados: {len(result['items'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no BusinessRulesCalculator: {e}")
        return False

def test_endpoint_logic():
    """Simula a lógica do endpoint calculate_simplified_budget"""
    print("\nTestando lógica do endpoint...")
    
    # Simular dados que viriam do frontend
    class MockBudgetData:
        def __init__(self):
            self.items = [MockItem()]
            self.outras_despesas_totais = 10.0
    
    class MockItem:
        def __init__(self):
            self.description = 'Item de teste'
            self.quantity = 1
            self.peso_compra = 10.0
            self.peso_venda = 10.0
            self.valor_com_icms_compra = 100.0
            self.percentual_icms_compra = 0.18
            self.outras_despesas_item = 5.0
            self.valor_com_icms_venda = 150.0
            self.percentual_icms_venda = 0.17
    
    budget_data = MockBudgetData()
    
    try:
        # Validação básica
        if not budget_data.items:
            raise ValueError("Orçamento deve ter pelo menos um item")
        
        # Converter dados dos itens para formato do calculador
        items_data = []
        for item in budget_data.items:
            item_dict = {
                'description': item.description,
                'quantity': item.quantity,
                'peso_compra': item.peso_compra,
                'peso_venda': item.peso_venda,
                'valor_com_icms_compra': item.valor_com_icms_compra,
                'percentual_icms_compra': item.percentual_icms_compra,
                'outras_despesas_item': getattr(item, 'outras_despesas_item', 0.0),
                'valor_com_icms_venda': item.valor_com_icms_venda,
                'percentual_icms_venda': item.percentual_icms_venda
            }
            items_data.append(item_dict)
        
        # Usar o BusinessRulesCalculator para cálculo completo
        calculator = BusinessRulesCalculator()
        result = calculator.calculate_complete_budget(
            items_data, 
            getattr(budget_data, 'outras_despesas_totais', 0.0)
        )
        
        # Preparar resposta no formato esperado pelo frontend
        items_calculations = []
        for item in result['items']:
            items_calculations.append({
                'description': item['description'],
                'quantity': item['quantity'],
                'peso_compra': item['peso_compra'],
                'peso_venda': item['peso_venda'],
                'total_compra_item': item['total_compra_item'],
                'total_venda_item': item['total_venda_item'],
                'rentabilidade_item': item['rentabilidade_item'],
                'percentual_comissao': item['percentual_comissao'],
                'valor_comissao': item['valor_comissao']
            })
        
        # Simular o BudgetCalculation response
        response = {
            'total_purchase_value': result['totals']['soma_total_compra'],
            'total_sale_value': result['totals']['soma_total_venda'],
            'total_commission': result['totals']['comissao_total_pedido'],
            'profitability_percentage': result['totals']['markup_pedido'],  # O markup é a rentabilidade
            'markup_percentage': result['totals']['markup_pedido'],
            'items_calculations': items_calculations
        }
        
        print("✓ Lógica do endpoint executada com sucesso")
        print(f"✓ Response preparado com {len(response['items_calculations'])} itens")
        print(f"✓ Total purchase value: {response['total_purchase_value']}")
        print(f"✓ Total sale value: {response['total_sale_value']}")
        print(f"✓ Total commission: {response['total_commission']}")
        print(f"✓ Profitability percentage: {response['profitability_percentage']}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na lógica do endpoint: {e}")
        return False

if __name__ == "__main__":
    print("=== TESTE DO ENDPOINT /api/v1/budgets/calculate-simplified ===\n")
    
    success1 = test_business_rules_calculator()
    success2 = test_endpoint_logic()
    
    if success1 and success2:
        print("\n✓ TODOS OS TESTES PASSARAM - O endpoint deve estar funcionando corretamente!")
        sys.exit(0)
    else:
        print("\n❌ ALGUNS TESTES FALHARAM - Há problemas a corrigir.")
        sys.exit(1)

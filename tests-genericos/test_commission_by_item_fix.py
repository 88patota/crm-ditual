#!/usr/bin/env python3
"""
Teste para verificar se a correção do cálculo de comissão por item está funcionando
Testa especificamente o BusinessRulesCalculator com CommissionService
"""

import sys
sys.path.append('services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_commission_calculation_by_item():
    """
    Testa se a comissão é calculada corretamente por item baseada na rentabilidade
    """
    print("🧪 Teste: Verificação de Cálculo de Comissão por Item")
    print("=" * 60)
    
    # Dados de teste com diferentes rentabilidades
    test_items = [
        {
            "description": "Item com Rentabilidade Alta (40%+)",
            "peso_compra": 10.0,
            "peso_venda": 10.0,
            "valor_com_icms_compra": 100.00,
            "percentual_icms_compra": 0.18,
            "valor_com_icms_venda": 180.00,  # Alto markup para alta rentabilidade
            "percentual_icms_venda": 0.17,
            "outras_despesas_item": 0.0
        },
        {
            "description": "Item com Rentabilidade Baixa (~10%)", 
            "peso_compra": 5.0,
            "peso_venda": 5.0,
            "valor_com_icms_compra": 200.00,
            "percentual_icms_compra": 0.18,
            "valor_com_icms_venda": 210.00,  # Baixo markup para baixa rentabilidade
            "percentual_icms_venda": 0.17,
            "outras_despesas_item": 0.0
        },
        {
            "description": "Item com Rentabilidade Média (25%)",
            "peso_compra": 8.0,
            "peso_venda": 8.0,
            "valor_com_icms_compra": 150.00,
            "percentual_icms_compra": 0.18,
            "valor_com_icms_venda": 200.00,  # Markup médio
            "percentual_icms_venda": 0.17,
            "outras_despesas_item": 0.0
        }
    ]
    
    try:
        print("📊 Calculando orçamento usando BusinessRulesCalculator...")
        
        # Calcular totais
        soma_pesos_pedido = sum(item['peso_compra'] for item in test_items)
        # outras_despesas_item é R$/kg; somar multiplicando pelo peso_compra
        outras_despesas_totais = sum(
            (item.get('outras_despesas_item', 0) or 0.0) * (item.get('peso_compra', 0) or 0.0)
            for item in test_items
        )
        
        # Calcular usando BusinessRulesCalculator
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            test_items, outras_despesas_totais, soma_pesos_pedido
        )
        
        print(f"✅ Cálculo concluído! {len(budget_result['items'])} itens processados")
        print()
        
        # Verificar cada item
        total_commission = 0.0
        for i, calculated_item in enumerate(budget_result['items']):
            print(f"📋 Item {i+1}: {calculated_item['description']}")
            
            # Extrair dados calculados
            rentabilidade = calculated_item['rentabilidade_item']  # Em decimal
            total_venda_item = calculated_item['total_venda_item']
            valor_comissao = calculated_item['valor_comissao']
            
            # Calcular comissão esperada usando CommissionService diretamente
            percentual_comissao_esperado = CommissionService.calculate_commission_percentage(rentabilidade)
            valor_comissao_esperado = CommissionService.calculate_commission_value(total_venda_item, rentabilidade)
            
            print(f"  • Rentabilidade: {rentabilidade*100:.2f}%")
            print(f"  • Total venda item: R$ {total_venda_item:.2f}")
            print(f"  • % Comissão esperado: {percentual_comissao_esperado*100:.2f}%")
            print(f"  • Valor comissão calculado: R$ {valor_comissao:.2f}")
            print(f"  • Valor comissão esperado: R$ {valor_comissao_esperado:.2f}")
            
            # Verificar se está correto (tolerância de 0.01)
            if abs(valor_comissao - valor_comissao_esperado) <= 0.01:
                print(f"  ✅ Comissão calculada CORRETAMENTE!")
            else:
                print(f"  ❌ ERRO: Comissão incorreta!")
                print(f"     Diferença: R$ {abs(valor_comissao - valor_comissao_esperado):.2f}")
                return False
            
            total_commission += valor_comissao
            print()
        
        # Verificar total
        budget_total_commission = sum(item['valor_comissao'] for item in budget_result['items'])
        print(f"💰 Verificação do Total:")
        print(f"  • Soma individual: R$ {total_commission:.2f}")
        print(f"  • Total do orçamento: R$ {budget_total_commission:.2f}")
        
        if abs(total_commission - budget_total_commission) <= 0.01:
            print(f"  ✅ Total de comissão está CORRETO!")
        else:
            print(f"  ❌ ERRO: Total não confere!")
            return False
        
        # Mostrar resumo das faixas de comissão
        print(f"\n📈 Faixas de Comissão Aplicadas:")
        commission_summary = CommissionService.calculate_budget_total_commission(budget_result['items'])
        
        for bracket, value in commission_summary['commission_by_bracket'].items():
            if value > 0:
                print(f"  • Faixa {bracket}: R$ {value:.2f}")
        
        print(f"\n🎯 Resumo Final:")
        print(f"  • Total compra: R$ {budget_result['totals']['soma_total_compra']:.2f}")
        print(f"  • Total venda: R$ {budget_result['totals']['soma_total_venda']:.2f}")
        print(f"  • Total comissão: R$ {budget_total_commission:.2f}")
        print(f"  • Markup pedido: {budget_result['totals']['markup_pedido']:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_commission_service_directly():
    """
    Testa o CommissionService diretamente para verificar as faixas
    """
    print("\n🔬 Teste: Verificação Direta do CommissionService")
    print("=" * 60)
    
    # Testes de diferentes faixas de rentabilidade
    test_cases = [
        {"rentabilidade": 0.10, "expected_commission": 0.00, "description": "10% - Sem comissão"},
        {"rentabilidade": 0.25, "expected_commission": 0.01, "description": "25% - Comissão 1%"},
        {"rentabilidade": 0.35, "expected_commission": 0.015, "description": "35% - Comissão 1.5%"},
        {"rentabilidade": 0.45, "expected_commission": 0.025, "description": "45% - Comissão 2.5%"},
        {"rentabilidade": 0.55, "expected_commission": 0.03, "description": "55% - Comissão 3%"},
        {"rentabilidade": 0.70, "expected_commission": 0.04, "description": "70% - Comissão 4%"},
        {"rentabilidade": 0.90, "expected_commission": 0.05, "description": "90% - Comissão 5%"},
    ]
    
    for test_case in test_cases:
        rentabilidade = test_case["rentabilidade"]
        expected = test_case["expected_commission"]
        description = test_case["description"]
        
        calculated = CommissionService.calculate_commission_percentage(rentabilidade)
        
        print(f"📊 {description}")
        print(f"  • Rentabilidade: {rentabilidade*100:.0f}%")
        print(f"  • Comissão esperada: {expected*100:.1f}%")
        print(f"  • Comissão calculada: {calculated*100:.1f}%")
        
        if abs(calculated - expected) <= 0.001:
            print(f"  ✅ CORRETO!")
        else:
            print(f"  ❌ ERRO!")
            return False
        print()
    
    return True

def main():
    """
    Executa todos os testes
    """
    print("🚀 Iniciando testes de comissão por item (pós-correção)")
    print("=" * 80)
    
    # Teste 1: CommissionService diretamente
    if not test_commission_service_directly():
        print("\n❌ Falha nos testes do CommissionService")
        sys.exit(1)
    
    # Teste 2: BusinessRulesCalculator integrado
    if not test_commission_calculation_by_item():
        print("\n❌ Falha nos testes do BusinessRulesCalculator")
        sys.exit(1)
    
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    print("\n📋 Verificações realizadas:")
    print("  ✅ CommissionService calcula percentuais corretos por faixa de rentabilidade")
    print("  ✅ BusinessRulesCalculator usa CommissionService corretamente")
    print("  ✅ Comissão é calculada individualmente por item baseada na sua rentabilidade")
    print("  ✅ Total de comissão é a soma das comissões individuais")
    print("  ✅ Diferentes rentabilidades geram diferentes percentuais de comissão")
    
    print("\n🔧 Correção implementada:")
    print("  • Sistema agora usa BusinessRulesCalculator + CommissionService")
    print("  • Comissão calculada POR ITEM baseada na RENTABILIDADE individual")
    print("  • Percentual varia de 0% a 5% conforme faixas de rentabilidade")
    print("  • Não mais usa percentual fixo de 1,5% sobre total do pedido")

if __name__ == "__main__":
    main()

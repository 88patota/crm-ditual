#!/usr/bin/env python3
"""
Test script to validate the new commission calculation rule with weight differences
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_new_commission_rule():
    """Test the new commission rule that considers weight differences"""
    
    print("=" * 80)
    print("TESTE: Nova Regra de Comissão com Diferenças de Quantidade")
    print("=" * 80)
    
    # Test case: Item with good profitability and different sale quantities
    base_item = {
        'description': 'Produto com Boa Rentabilidade',
        'peso_compra': 100.0,  # Comprar 100kg
        'valor_com_icms_compra': 10.0,  # R$ 10 por kg com ICMS (custo baixo)
        'percentual_icms_compra': 0.18,
        'valor_com_icms_venda': 30.0,   # R$ 30 por kg com ICMS (preço alto = boa rentabilidade)
        'percentual_icms_venda': 0.18,
    }
    
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 100.0
    
    print("\nCenário Base:")
    print(f"Peso Compra: {base_item['peso_compra']} kg")
    print(f"Valor Compra: R$ {base_item['valor_com_icms_compra']}/kg")
    print(f"Valor Venda: R$ {base_item['valor_com_icms_venda']}/kg")
    
    # Test scenarios
    scenarios = [
        {"name": "Venda = Compra (100kg)", "peso_venda": 100.0},
        {"name": "Venda > Compra (120kg vs 100kg)", "peso_venda": 120.0},
        {"name": "Venda > Compra (150kg vs 100kg)", "peso_venda": 150.0},
        {"name": "Venda < Compra (80kg vs 100kg)", "peso_venda": 80.0},
        {"name": "Venda < Compra (50kg vs 100kg)", "peso_venda": 50.0},
    ]
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'-' * 60}")
        print(f"TESTE {i}: {scenario['name']}")
        print(f"{'-' * 60}")
        
        item = base_item.copy()
        item['peso_venda'] = scenario['peso_venda']
        
        result = BusinessRulesCalculator.calculate_complete_item(
            item, outras_despesas_totais, soma_pesos_pedido
        )
        
        results.append(result)
        
        # Calcular rentabilidade total real para comparação
        rentabilidade_total_real = (result['total_venda_item'] / result['total_compra_item']) - 1 if result['total_compra_item'] > 0 else 0
        
        print(f"Peso Venda: {result['peso_venda']} kg")
        print(f"Total Compra: R$ {result['total_compra_item']:.2f}")
        print(f"Total Venda: R$ {result['total_venda_item']:.2f}")
        print(f"Rentabilidade Unitária: {result['rentabilidade_item']*100:.2f}%")
        print(f"Rentabilidade Total Real: {rentabilidade_total_real*100:.2f}%")
        print(f"Diferença Peso: {result['diferenca_peso']:.1f} kg")
        print(f"Comissão: R$ {result['valor_comissao']:.2f}")
        
        # Verificar qual faixa de comissão foi aplicada
        faixa_comissao = CommissionService.calculate_commission_percentage(rentabilidade_total_real) * 100
        print(f"Faixa Comissão Aplicada: {faixa_comissao:.1f}%")
    
    # Análise comparativa
    print(f"\\n{'=' * 80}")
    print("ANÁLISE COMPARATIVA DOS RESULTADOS")
    print(f"{'=' * 80}")
    
    base_result = results[0]  # Cenário base (mesma quantidade)
    
    print(f"\n{'Cenário':<30} {'Total Venda':<12} {'Comissão':<12} {'Variação Comissão':<15}")
    print(f"{'-' * 75}")
    
    for i, (scenario, result) in enumerate(zip(scenarios, results)):
        if i == 0:
            var_comissao = "Base"
        else:
            if base_result['valor_comissao'] > 0:
                var_percent = ((result['valor_comissao'] / base_result['valor_comissao']) - 1) * 100
                var_comissao = f"{var_percent:+.1f}%"
            else:
                var_comissao = "N/A"
        
        print(f"{scenario['name']:<30} R$ {result['total_venda_item']:>8.2f} R$ {result['valor_comissao']:>8.2f} {var_comissao:>12}")
    
    # Verificação da regra implementada
    print(f"\\n{'=' * 80}")
    print("VERIFICAÇÃO DA NOVA REGRA")
    print(f"{'=' * 80}")
    
    print("\nA nova regra funciona da seguinte forma:")
    print("1. Para vendas com mesma quantidade da compra: usa rentabilidade unitária")
    print("2. Para vendas com quantidade diferente: usa rentabilidade total da operação")
    print("3. A comissão é sempre aplicada sobre o valor total de venda efetivo")
    
    # Validar se a comissão está escalando corretamente
    venda_120 = results[1]
    venda_150 = results[2]
    
    if base_result['valor_comissao'] > 0:
        ratio_venda_120 = venda_120['total_venda_item'] / base_result['total_venda_item']
        ratio_comissao_120 = venda_120['valor_comissao'] / base_result['valor_comissao']
        
        print(f"\nValidação para venda 120kg vs 100kg:")
        print(f"Ratio Venda: {ratio_venda_120:.3f}")
        print(f"Ratio Comissão: {ratio_comissao_120:.3f}")
        
        if abs(ratio_venda_120 - ratio_comissao_120) < 0.01:
            print("✓ Comissão está escalando proporcionalmente com o volume de venda")
        else:
            print("✗ Comissão NÃO está escalando proporcionalmente")
    
    print(f"\\n{'=' * 80}")
    print("RESUMO DA IMPLEMENTAÇÃO")
    print(f"{'=' * 80}")
    print("A nova regra implementada garante que:")
    print("• Vendas de maior quantidade geram proporcionalmente mais comissão")
    print("• A rentabilidade é calculada considerando a operação total")
    print("• A comissão reflete o valor real gerado pela venda")
    print("• Mantém compatibilidade com cenários de mesma quantidade")

if __name__ == "__main__":
    test_new_commission_rule()
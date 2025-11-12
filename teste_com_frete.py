#!/usr/bin/env python3
"""
Teste para verificar se o frete está sendo incluído corretamente no cálculo
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def teste_com_frete():
    """Testa o cálculo incluindo o frete conforme payload do usuário"""
    
    print("=== TESTE COM FRETE INCLUÍDO ===")
    
    # Dados do payload do usuário
    items_data = [
        {
            'peso_compra': 1000,
            'peso_venda': 1010,
            'valor_com_icms_compra': 2.11,
            'valor_com_icms_venda': 4.32,
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'percentual_ipi': 0.0,
            'outras_despesas_item': 0.0
        },
        {
            'peso_compra': 1000,
            'peso_venda': 1010,
            'valor_com_icms_compra': 2.11,
            'valor_com_icms_venda': 4.32,
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'percentual_ipi': 0.0,
            'outras_despesas_item': 0.0
        }
    ]
    
    # Parâmetros do orçamento
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 2020.0  # 2 × 1010kg (peso de venda)
    freight_value_total = 500.0  # Frete informado no payload
    
    print(f"Frete total: R$ {freight_value_total:.2f}")
    print(f"Soma pesos pedido: {soma_pesos_pedido:.1f} kg")
    print(f"Frete por kg: R$ {freight_value_total / soma_pesos_pedido:.6f}")
    
    print("\n=== TESTE SEM FRETE ===")
    resultado_sem_frete = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido, 0.0
    )
    
    print(f"Total compra SEM frete: R$ {resultado_sem_frete['totals']['soma_total_compra']:.2f}")
    print(f"Total venda: R$ {resultado_sem_frete['totals']['soma_total_venda']:.2f}")
    
    rentabilidade_sem_frete = (resultado_sem_frete['totals']['soma_total_venda'] - resultado_sem_frete['totals']['soma_total_compra']) / resultado_sem_frete['totals']['soma_total_compra']
    print(f"Rentabilidade SEM frete: {rentabilidade_sem_frete:.4f} = {rentabilidade_sem_frete*100:.2f}%")
    
    print("\n=== TESTE COM FRETE ===")
    resultado_com_frete = BusinessRulesCalculator.calculate_complete_budget(
        items_data, outras_despesas_totais, soma_pesos_pedido, freight_value_total
    )
    
    print(f"Total compra COM frete: R$ {resultado_com_frete['totals']['soma_total_compra']:.2f}")
    print(f"Total venda: R$ {resultado_com_frete['totals']['soma_total_venda']:.2f}")
    
    rentabilidade_com_frete = (resultado_com_frete['totals']['soma_total_venda'] - resultado_com_frete['totals']['soma_total_compra']) / resultado_com_frete['totals']['soma_total_compra']
    print(f"Rentabilidade COM frete: {rentabilidade_com_frete:.4f} = {rentabilidade_com_frete*100:.2f}%")
    
    # Verificar se há campo de frete nos totais
    if 'valor_frete_compra' in resultado_com_frete['totals']:
        print(f"Valor frete por kg nos totais: R$ {resultado_com_frete['totals']['valor_frete_compra']:.6f}")
    
    print("\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    total_compra_esperado = 3640.314
    total_venda_esperado = 6493.75056
    rentabilidade_esperada = 0.7838435255859797
    
    print(f"Total compra esperado: R$ {total_compra_esperado:.2f}")
    print(f"Total compra calculado: R$ {resultado_com_frete['totals']['soma_total_compra']:.2f}")
    print(f"Diferença compra: R$ {abs(total_compra_esperado - resultado_com_frete['totals']['soma_total_compra']):.2f}")
    
    print(f"Total venda esperado: R$ {total_venda_esperado:.2f}")
    print(f"Total venda calculado: R$ {resultado_com_frete['totals']['soma_total_venda']:.2f}")
    print(f"Diferença venda: R$ {abs(total_venda_esperado - resultado_com_frete['totals']['soma_total_venda']):.2f}")
    
    print(f"Rentabilidade esperada: {rentabilidade_esperada:.6f} = {rentabilidade_esperada*100:.2f}%")
    print(f"Rentabilidade calculada: {rentabilidade_com_frete:.6f} = {rentabilidade_com_frete*100:.2f}%")
    print(f"Diferença rentabilidade: {abs(rentabilidade_esperada - rentabilidade_com_frete):.6f}")
    
    if abs(rentabilidade_esperada - rentabilidade_com_frete) < 0.001:
        print("✅ SUCESSO! A rentabilidade COM frete bate com a esperada!")
        
        # Verificar se a comissão também está correta
        markup_calculado = resultado_com_frete['totals']['markup_pedido']
        print(f"\nMarkup calculado: {markup_calculado:.4f} = {markup_calculado*100:.2f}%")
        
        # Calcular taxa de comissão baseada na rentabilidade
        from app.services.commission_service import CommissionService
        
        # Usar o primeiro item para calcular a comissão
        item_resultado = resultado_com_frete['items'][0]
        taxa_comissao = CommissionService.calculate_commission_rate(item_resultado['rentabilidade_item'])
        
        print(f"Taxa de comissão calculada: {taxa_comissao:.1f}%")
        
        if abs(taxa_comissao - 4.0) < 0.1:
            print("✅ Taxa de comissão também está correta (4%)!")
        else:
            print(f"❌ Taxa de comissão deveria ser 4%, mas é {taxa_comissao:.1f}%")
    else:
        print("❌ Ainda há diferença na rentabilidade")

if __name__ == "__main__":
    teste_com_frete()
#!/usr/bin/env python3
"""
Debug detalhado do cálculo de venda para entender a diferença
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def debug_venda():
    """Debug detalhado do cálculo de venda"""
    
    print("=== DEBUG DETALHADO DO CÁLCULO DE VENDA ===")
    
    # Dados do item
    valor_com_icms_venda = 4.32
    percentual_icms_venda = 0.18
    peso_venda = 1010
    
    print(f"Valor com ICMS venda: R$ {valor_com_icms_venda:.2f}")
    print(f"ICMS venda: {percentual_icms_venda*100:.0f}%")
    print(f"Peso venda: {peso_venda} kg")
    
    # Cálculo manual do valor de venda
    valor_sem_icms_venda = valor_com_icms_venda * (1 - percentual_icms_venda)
    print(f"Valor sem ICMS venda: R$ {valor_sem_icms_venda:.6f}")
    
    # PIS/COFINS na venda
    pis_cofins = 0.0925
    valor_sem_impostos_venda = valor_sem_icms_venda * (1 - pis_cofins)
    print(f"Valor sem impostos venda (após PIS/COFINS): R$ {valor_sem_impostos_venda:.6f}")
    
    # Total venda por item
    total_venda_item = valor_sem_impostos_venda * peso_venda
    print(f"Total venda item: R$ {total_venda_item:.6f}")
    
    # Total venda 2 itens
    total_venda_2_itens = total_venda_item * 2
    print(f"Total venda 2 itens: R$ {total_venda_2_itens:.2f}")
    
    # Verificar se o sistema calcula igual
    print("\n=== COMPARAÇÃO COM SISTEMA ===")
    
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
    
    resultado = BusinessRulesCalculator.calculate_complete_budget(
        items_data, 0.0, 2020.0, 500.0
    )
    
    total_venda_sistema = resultado['totals']['soma_total_venda']
    print(f"Total venda sistema: R$ {total_venda_sistema:.2f}")
    print(f"Total venda manual: R$ {total_venda_2_itens:.2f}")
    print(f"Diferença venda: R$ {abs(total_venda_sistema - total_venda_2_itens):.6f}")
    
    # Verificar se o sistema usa valores COM ICMS para venda
    print("\n=== TESTE: VENDA COM ICMS (SEM DESCONTAR IMPOSTOS) ===")
    total_venda_com_icms = valor_com_icms_venda * peso_venda * 2
    print(f"Total venda COM ICMS: R$ {total_venda_com_icms:.2f}")
    
    if abs(total_venda_sistema - total_venda_com_icms) < 0.01:
        print("✅ O sistema usa valores COM ICMS para venda!")
        
        # Recalcular rentabilidade usando venda COM ICMS
        print("\n=== RENTABILIDADE COM VENDA COM ICMS ===")
        total_compra_sistema = resultado['totals']['soma_total_compra']
        rentabilidade_com_icms = (total_venda_com_icms - total_compra_sistema) / total_compra_sistema
        
        print(f"Total compra sistema: R$ {total_compra_sistema:.2f}")
        print(f"Total venda COM ICMS: R$ {total_venda_com_icms:.2f}")
        print(f"Rentabilidade COM ICMS: {rentabilidade_com_icms:.6f} = {rentabilidade_com_icms*100:.2f}%")
        
        rentabilidade_esperada = 0.7838435255859797
        diferenca_rent = abs(rentabilidade_esperada - rentabilidade_com_icms)
        print(f"Rentabilidade esperada: {rentabilidade_esperada:.6f} = {rentabilidade_esperada*100:.2f}%")
        print(f"Diferença: {diferenca_rent:.6f}")
        
        if diferenca_rent < 0.001:
            print("✅ RENTABILIDADE PERFEITA!")
        else:
            print("❌ Ainda há diferença")
    
    # Verificar valores esperados do usuário
    print("\n=== COMPARAÇÃO COM VALORES ESPERADOS DO USUÁRIO ===")
    total_compra_esperado = 3640.314
    total_venda_esperado = 6493.75056
    
    print(f"Total compra esperado: R$ {total_compra_esperado:.3f}")
    print(f"Total venda esperado: R$ {total_venda_esperado:.3f}")
    
    rentabilidade_esperada_usuario = (total_venda_esperado - total_compra_esperado) / total_compra_esperado
    print(f"Rentabilidade esperada usuário: {rentabilidade_esperada_usuario:.6f} = {rentabilidade_esperada_usuario*100:.2f}%")
    
    # Verificar se o total de venda esperado bate com COM ICMS
    if abs(total_venda_esperado - total_venda_com_icms) < 1.0:
        print("✅ Total venda esperado bate com valores COM ICMS!")
    else:
        print(f"❌ Diferença no total venda: R$ {abs(total_venda_esperado - total_venda_com_icms):.2f}")

if __name__ == "__main__":
    debug_venda()
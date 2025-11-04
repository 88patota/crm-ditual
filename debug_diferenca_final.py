#!/usr/bin/env python3
"""
Debug para entender a diferença de R$ 4.95 no total de compra
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

def debug_diferenca():
    """Debug detalhado da diferença"""
    
    print("=== DEBUG DA DIFERENÇA DE R$ 4.95 ===")
    
    # Dados do payload do usuário
    item_data = {
        'peso_compra': 1000,
        'peso_venda': 1010,
        'valor_com_icms_compra': 2.11,
        'valor_com_icms_venda': 4.32,
        'percentual_icms_compra': 0.18,
        'percentual_icms_venda': 0.18,
        'percentual_ipi': 0.0,
        'outras_despesas_item': 0.0
    }
    
    # Parâmetros
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 2020.0  # 2 × 1010kg
    freight_value_total = 500.0
    
    print(f"Frete total: R$ {freight_value_total:.2f}")
    print(f"Soma pesos pedido: {soma_pesos_pedido:.1f} kg")
    
    # Calcular frete por kg
    frete_por_kg = freight_value_total / soma_pesos_pedido
    print(f"Frete por kg: R$ {frete_por_kg:.6f}")
    
    # Calcular um item detalhadamente
    print("\n=== CÁLCULO DETALHADO DE UM ITEM ===")
    
    # Valor sem ICMS de compra
    valor_sem_icms_compra = item_data['valor_com_icms_compra'] / (1 + item_data['percentual_icms_compra'])
    print(f"Valor sem ICMS compra: R$ {valor_sem_icms_compra:.6f}")
    
    # Valor sem impostos (incluindo frete)
    valor_sem_impostos_compra = BusinessRulesCalculator.calculate_purchase_value_without_taxes(
        item_data['valor_com_icms_compra'], 
        item_data['percentual_icms_compra'], 
        frete_por_kg
    )
    print(f"Valor sem impostos + frete: R$ {valor_sem_impostos_compra:.6f}")
    
    # Valor corrigido por peso
    valor_corrigido_peso = BusinessRulesCalculator.calculate_purchase_value_with_weight_correction(
        valor_sem_impostos_compra, 
        item_data['peso_compra'], 
        item_data['peso_venda']
    )
    print(f"Valor corrigido peso: R$ {valor_corrigido_peso:.6f}")
    
    # Total por item
    total_compra_item = valor_corrigido_peso * item_data['peso_venda']
    print(f"Total compra item: R$ {total_compra_item:.6f}")
    
    # Total para 2 itens
    total_compra_2_itens = total_compra_item * 2
    print(f"Total compra 2 itens: R$ {total_compra_2_itens:.2f}")
    
    print("\n=== COMPARAÇÃO COM VALORES ESPERADOS ===")
    total_esperado = 3640.314
    diferenca = abs(total_esperado - total_compra_2_itens)
    print(f"Total esperado: R$ {total_esperado:.3f}")
    print(f"Total calculado: R$ {total_compra_2_itens:.3f}")
    print(f"Diferença: R$ {diferenca:.3f}")
    
    # Verificar se a diferença está na precisão decimal
    print("\n=== ANÁLISE DA PRECISÃO ===")
    
    # Calcular manualmente com mais precisão
    valor_base = 2.11 / 1.18  # Valor sem ICMS
    valor_com_frete = valor_base + frete_por_kg
    fator_correcao = 1010 / 1000  # Correção de peso
    valor_final_por_kg = valor_com_frete * fator_correcao
    total_manual = valor_final_por_kg * 1010 * 2  # 2 itens
    
    print(f"Cálculo manual:")
    print(f"  Valor base (sem ICMS): R$ {valor_base:.6f}")
    print(f"  Valor com frete: R$ {valor_com_frete:.6f}")
    print(f"  Fator correção peso: {fator_correcao:.6f}")
    print(f"  Valor final por kg: R$ {valor_final_por_kg:.6f}")
    print(f"  Total manual: R$ {total_manual:.6f}")
    
    diferenca_manual = abs(total_esperado - total_manual)
    print(f"  Diferença manual: R$ {diferenca_manual:.6f}")
    
    # Testar com peso de compra em vez de venda para o frete
    print("\n=== TESTE COM PESO DE COMPRA PARA FRETE ===")
    soma_pesos_compra = 2000.0  # 2 × 1000kg
    frete_por_kg_compra = freight_value_total / soma_pesos_compra
    print(f"Frete por kg (base peso compra): R$ {frete_por_kg_compra:.6f}")
    
    valor_com_frete_compra = valor_base + frete_por_kg_compra
    total_com_peso_compra = valor_com_frete_compra * fator_correcao * 1010 * 2
    print(f"Total com peso compra: R$ {total_com_peso_compra:.6f}")
    
    diferenca_peso_compra = abs(total_esperado - total_com_peso_compra)
    print(f"Diferença peso compra: R$ {diferenca_peso_compra:.6f}")
    
    if diferenca_peso_compra < diferenca:
        print("✅ Usar peso de compra para distribuir frete reduz a diferença!")
    else:
        print("❌ Usar peso de venda para frete é melhor")

if __name__ == "__main__":
    debug_diferenca()
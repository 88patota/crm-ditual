#!/usr/bin/env python3
"""
Cálculo correto incluindo PIS/COFINS de 9.25%
"""

def calculo_correto():
    """Cálculo correto com PIS/COFINS"""
    
    print("=== CÁLCULO CORRETO COM PIS/COFINS ===")
    
    # Dados do item
    valor_com_icms_compra = 2.11
    percentual_icms_compra = 0.18
    peso_compra = 1000
    peso_venda = 1010
    
    # Frete
    freight_value_total = 500.0
    soma_pesos_pedido = 2020.0  # 2 × 1010kg (peso de venda)
    frete_por_kg = freight_value_total / soma_pesos_pedido
    
    print(f"Valor com ICMS compra: R$ {valor_com_icms_compra:.2f}")
    print(f"ICMS: {percentual_icms_compra*100:.0f}%")
    print(f"Frete por kg: R$ {frete_por_kg:.6f}")
    
    # Passo 1: Remover ICMS
    valor_sem_icms = valor_com_icms_compra * (1 - percentual_icms_compra)
    print(f"Valor sem ICMS: R$ {valor_sem_icms:.6f}")
    
    # Passo 2: Remover PIS/COFINS (9.25%)
    pis_cofins = 0.0925
    valor_sem_impostos = valor_sem_icms * (1 - pis_cofins)
    print(f"Valor sem impostos (após PIS/COFINS): R$ {valor_sem_impostos:.6f}")
    
    # Passo 3: Adicionar frete
    valor_com_frete = valor_sem_impostos + frete_por_kg
    print(f"Valor com frete: R$ {valor_com_frete:.6f}")
    
    # Passo 4: Correção de peso
    fator_correcao = peso_venda / peso_compra
    valor_corrigido = valor_com_frete * fator_correcao
    print(f"Valor corrigido peso: R$ {valor_corrigido:.6f}")
    
    # Passo 5: Total por item
    total_item = valor_corrigido * peso_venda
    print(f"Total por item: R$ {total_item:.6f}")
    
    # Passo 6: Total para 2 itens
    total_2_itens = total_item * 2
    print(f"Total 2 itens: R$ {total_2_itens:.2f}")
    
    # Comparação
    total_esperado = 3640.314
    diferenca = abs(total_esperado - total_2_itens)
    print(f"\nTotal esperado: R$ {total_esperado:.3f}")
    print(f"Total calculado: R$ {total_2_itens:.3f}")
    print(f"Diferença: R$ {diferenca:.3f}")
    
    # Calcular rentabilidade
    # Valor de venda (sem impostos)
    valor_com_icms_venda = 4.32
    percentual_icms_venda = 0.18
    valor_sem_icms_venda = valor_com_icms_venda * (1 - percentual_icms_venda)
    valor_sem_impostos_venda = valor_sem_icms_venda * (1 - pis_cofins)
    total_venda_item = valor_sem_impostos_venda * peso_venda
    total_venda_2_itens = total_venda_item * 2
    
    print(f"\nTotal venda 2 itens: R$ {total_venda_2_itens:.2f}")
    
    rentabilidade = (total_venda_2_itens - total_2_itens) / total_2_itens
    print(f"Rentabilidade calculada: {rentabilidade:.6f} = {rentabilidade*100:.2f}%")
    
    rentabilidade_esperada = 0.7838435255859797
    print(f"Rentabilidade esperada: {rentabilidade_esperada:.6f} = {rentabilidade_esperada*100:.2f}%")
    
    diferenca_rent = abs(rentabilidade_esperada - rentabilidade)
    print(f"Diferença rentabilidade: {diferenca_rent:.6f}")
    
    if diferenca_rent < 0.001:
        print("✅ RENTABILIDADE CORRETA!")
    else:
        print("❌ Ainda há diferença na rentabilidade")
        
    # Verificar se o problema está no peso usado para distribuir o frete
    print("\n=== TESTE: FRETE BASEADO NO PESO DE COMPRA ===")
    soma_pesos_compra = 2000.0  # 2 × 1000kg
    frete_por_kg_compra = freight_value_total / soma_pesos_compra
    print(f"Frete por kg (peso compra): R$ {frete_por_kg_compra:.6f}")
    
    valor_com_frete_compra = valor_sem_impostos + frete_por_kg_compra
    valor_corrigido_compra = valor_com_frete_compra * fator_correcao
    total_item_compra = valor_corrigido_compra * peso_venda
    total_2_itens_compra = total_item_compra * 2
    
    print(f"Total 2 itens (frete peso compra): R$ {total_2_itens_compra:.2f}")
    diferenca_compra = abs(total_esperado - total_2_itens_compra)
    print(f"Diferença (frete peso compra): R$ {diferenca_compra:.3f}")
    
    if diferenca_compra < diferenca:
        print("✅ Usar peso de compra para frete é melhor!")
        
        # Recalcular rentabilidade
        rentabilidade_compra = (total_venda_2_itens - total_2_itens_compra) / total_2_itens_compra
        print(f"Rentabilidade (frete peso compra): {rentabilidade_compra:.6f} = {rentabilidade_compra*100:.2f}%")
        
        diferenca_rent_compra = abs(rentabilidade_esperada - rentabilidade_compra)
        print(f"Diferença rentabilidade (frete peso compra): {diferenca_rent_compra:.6f}")
        
        if diferenca_rent_compra < 0.001:
            print("✅ RENTABILIDADE PERFEITA COM FRETE BASEADO NO PESO DE COMPRA!")

if __name__ == "__main__":
    calculo_correto()
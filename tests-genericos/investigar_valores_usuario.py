#!/usr/bin/env python3
"""
Investigação detalhada dos valores fornecidos pelo usuário
"""

def investigar_valores_usuario():
    """Investigar como o usuário chegou aos valores totais"""
    
    # Dados do payload
    total_compra_informado = 3640.314
    total_venda_informado = 6493.75056
    rentabilidade_informada = 0.7838435255859797
    
    # Dados dos itens
    peso_compra = 1000  # por item
    peso_venda = 1010   # por item
    valor_com_icms_compra = 2.11  # por kg
    valor_com_icms_venda = 4.32   # por kg
    
    print("=== INVESTIGAÇÃO DOS VALORES DO USUÁRIO ===")
    print(f"Total compra informado: R$ {total_compra_informado:.2f}")
    print(f"Total venda informado: R$ {total_venda_informado:.2f}")
    print(f"Rentabilidade informada: {rentabilidade_informada:.6f} = {rentabilidade_informada*100:.2f}%")
    
    print("\n=== VERIFICAÇÃO DA RENTABILIDADE ===")
    # Verificar se a rentabilidade bate com os totais informados
    rentabilidade_calculada_totais = (total_venda_informado - total_compra_informado) / total_compra_informado
    print(f"Rentabilidade dos totais: ({total_venda_informado:.2f} - {total_compra_informado:.2f}) / {total_compra_informado:.2f} = {rentabilidade_calculada_totais:.6f}")
    print(f"Rentabilidade informada: {rentabilidade_informada:.6f}")
    print(f"Diferença: {abs(rentabilidade_calculada_totais - rentabilidade_informada):.6f}")
    
    if abs(rentabilidade_calculada_totais - rentabilidade_informada) < 0.000001:
        print("✅ A rentabilidade informada BATE com os totais!")
    else:
        print("❌ A rentabilidade informada NÃO bate com os totais!")
    
    print("\n=== TENTATIVAS DE EXPLICAÇÃO ===")
    
    # Hipótese 1: Valores são SEM ICMS
    print("1. HIPÓTESE: Os totais são SEM ICMS")
    icms = 0.18
    valor_sem_icms_compra = valor_com_icms_compra / (1 + icms)
    valor_sem_icms_venda = valor_com_icms_venda / (1 + icms)
    
    total_compra_sem_icms = 2 * peso_compra * valor_sem_icms_compra
    total_venda_sem_icms = 2 * peso_venda * valor_sem_icms_venda
    
    print(f"   Valor unitário compra SEM ICMS: R$ {valor_sem_icms_compra:.6f}")
    print(f"   Valor unitário venda SEM ICMS: R$ {valor_sem_icms_venda:.6f}")
    print(f"   Total compra SEM ICMS: R$ {total_compra_sem_icms:.2f}")
    print(f"   Total venda SEM ICMS: R$ {total_venda_sem_icms:.2f}")
    print(f"   Diferença compra: R$ {abs(total_compra_informado - total_compra_sem_icms):.2f}")
    print(f"   Diferença venda: R$ {abs(total_venda_informado - total_venda_sem_icms):.2f}")
    
    # Hipótese 2: Há correção de peso aplicada
    print("\n2. HIPÓTESE: Há correção de peso aplicada")
    # Se o valor de compra for corrigido pelo peso
    valor_compra_corrigido = valor_sem_icms_compra * (peso_compra / peso_venda)
    total_compra_corrigido = 2 * peso_venda * valor_compra_corrigido  # Usar peso_venda para o total
    
    print(f"   Valor compra corrigido por peso: R$ {valor_compra_corrigido:.6f}")
    print(f"   Total compra com correção: R$ {total_compra_corrigido:.2f}")
    print(f"   Diferença: R$ {abs(total_compra_informado - total_compra_corrigido):.2f}")
    
    # Hipótese 3: Há PIS/COFINS aplicado
    print("\n3. HIPÓTESE: Há PIS/COFINS aplicado (9.25%)")
    pis_cofins = 0.0925
    valor_sem_impostos_compra = valor_com_icms_compra / (1 + icms) * (1 - pis_cofins)
    valor_sem_impostos_venda = valor_com_icms_venda / (1 + icms) * (1 - pis_cofins)
    
    total_compra_sem_impostos = 2 * peso_compra * valor_sem_impostos_compra
    total_venda_sem_impostos = 2 * peso_venda * valor_sem_impostos_venda
    
    print(f"   Valor unitário compra SEM impostos: R$ {valor_sem_impostos_compra:.6f}")
    print(f"   Valor unitário venda SEM impostos: R$ {valor_sem_impostos_venda:.6f}")
    print(f"   Total compra SEM impostos: R$ {total_compra_sem_impostos:.2f}")
    print(f"   Total venda SEM impostos: R$ {total_venda_sem_impostos:.2f}")
    print(f"   Diferença compra: R$ {abs(total_compra_informado - total_compra_sem_impostos):.2f}")
    print(f"   Diferença venda: R$ {abs(total_venda_informado - total_venda_sem_impostos):.2f}")
    
    # Hipótese 4: Combinação de PIS/COFINS + correção de peso
    print("\n4. HIPÓTESE: PIS/COFINS + correção de peso")
    valor_compra_sem_impostos_corrigido = valor_sem_impostos_compra * (peso_compra / peso_venda)
    total_compra_final = 2 * peso_venda * valor_compra_sem_impostos_corrigido
    
    print(f"   Valor compra SEM impostos + correção: R$ {valor_compra_sem_impostos_corrigido:.6f}")
    print(f"   Total compra final: R$ {total_compra_final:.2f}")
    print(f"   Diferença: R$ {abs(total_compra_informado - total_compra_final):.2f}")
    
    if abs(total_compra_informado - total_compra_final) < 1.0:
        print("   ✅ POSSÍVEL EXPLICAÇÃO ENCONTRADA!")
        
        rentabilidade_final = (total_venda_sem_impostos - total_compra_final) / total_compra_final
        print(f"   Rentabilidade com esta base: {rentabilidade_final:.6f} = {rentabilidade_final*100:.2f}%")
        print(f"   Diferença da informada: {abs(rentabilidade_final - rentabilidade_informada):.6f}")
    
    print("\n=== CONCLUSÃO ===")
    print("O usuário provavelmente está usando:")
    print("- Valores SEM ICMS e SEM PIS/COFINS para os totais")
    print("- Correção de peso aplicada no valor de compra")
    print("- Peso de venda para calcular o total final")

if __name__ == "__main__":
    investigar_valores_usuario()
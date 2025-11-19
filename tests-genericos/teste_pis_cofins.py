#!/usr/bin/env python3
"""
Teste para verificar se o problema é a aplicação do PIS/COFINS
"""

def teste_pis_cofins():
    """Teste comparando cálculos com e sem PIS/COFINS"""
    
    print("=== TESTE PIS/COFINS ===")
    
    # Dados do usuário
    valor_com_icms_compra = 2.11
    percentual_icms_compra = 0.18
    peso_compra = 1000
    peso_venda = 1010
    frete_total = 500
    
    print(f"Valor com ICMS compra: R$ {valor_com_icms_compra}")
    print(f"Percentual ICMS compra: {percentual_icms_compra * 100}%")
    print(f"Peso compra: {peso_compra} kg")
    print(f"Peso venda: {peso_venda} kg")
    print(f"Frete total: R$ {frete_total}")
    
    # Frete por kg
    frete_por_kg = frete_total / peso_venda
    print(f"Frete por kg: R$ {frete_por_kg:.6f}")
    
    print("\n=== CÁLCULO SEM PIS/COFINS (FRONTEND) ===")
    # Cálculo como o frontend faz (sem PIS/COFINS)
    valor_sem_icms = valor_com_icms_compra / (1 + percentual_icms_compra)
    valor_com_frete = valor_sem_icms + frete_por_kg
    total_compra_frontend = valor_com_frete * peso_compra
    
    print(f"Valor sem ICMS: R$ {valor_sem_icms:.6f}")
    print(f"Valor com frete: R$ {valor_com_frete:.6f}")
    print(f"Total compra: R$ {total_compra_frontend:.2f}")
    
    print("\n=== CÁLCULO COM PIS/COFINS (BUSINESSRULESCALCULATOR) ===")
    # Cálculo como o BusinessRulesCalculator faz (com PIS/COFINS)
    PIS_COFINS_PERCENTAGE = 0.0925  # 9.25%
    
    valor_sem_icms_calc = valor_com_icms_compra * (1 - percentual_icms_compra)
    valor_sem_impostos_calc = valor_sem_icms_calc * (1 - PIS_COFINS_PERCENTAGE)
    valor_com_frete_calc = valor_sem_impostos_calc + frete_por_kg
    total_compra_calc = valor_com_frete_calc * peso_compra
    
    print(f"Valor sem ICMS: R$ {valor_sem_icms_calc:.6f}")
    print(f"Valor sem impostos (com PIS/COFINS): R$ {valor_sem_impostos_calc:.6f}")
    print(f"Valor com frete: R$ {valor_com_frete_calc:.6f}")
    print(f"Total compra: R$ {total_compra_calc:.2f}")
    
    print("\n=== COMPARAÇÃO ===")
    diferenca = abs(total_compra_calc - total_compra_frontend)
    print(f"Diferença: R$ {diferenca:.2f}")
    
    # Verificar se a diferença bate com o que observamos
    diferenca_observada = 2070.16 - 2065.21
    print(f"Diferença observada nos testes: R$ {diferenca_observada:.2f}")
    
    if abs(diferenca - diferenca_observada) < 0.1:
        print("✅ CONFIRMADO: O problema é a aplicação do PIS/COFINS!")
    else:
        print("❌ Não é só o PIS/COFINS, há outro problema.")
    
    print("\n=== ANÁLISE ===")
    print("O BusinessRulesCalculator aplica:")
    print("1. Desconto ICMS: valor_com_icms * (1 - 0.18)")
    print("2. Desconto PIS/COFINS: resultado_anterior * (1 - 0.0925)")
    print("3. Soma frete")
    print()
    print("O frontend/backend parece aplicar apenas:")
    print("1. Desconto ICMS: valor_com_icms / (1 + 0.18)")
    print("2. Soma frete")
    print()
    print("Isso explica a diferença de R$ 4.95 no total de compra.")

if __name__ == "__main__":
    teste_pis_cofins()
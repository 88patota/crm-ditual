#!/usr/bin/env python3
"""
Teste para verificar se o cálculo das outras despesas foi corrigido
"""

# Dados do teste
peso_compra = 1000
valor_com_icms_compra = 2.12
percentual_icms_compra = 0.12
outras_despesas_item = 100
peso_venda = 1000
valor_com_icms_venda = 9.22
percentual_icms_venda = 0.12

# Constantes do sistema
PIS_COFINS_PERCENTAGE = 0.0925

print("=== TESTE DO CÁLCULO CORRIGIDO ===")
print(f"Peso compra: {peso_compra} kg")
print(f"Valor com ICMS compra: R$ {valor_com_icms_compra}")
print(f"Percentual ICMS compra: {percentual_icms_compra * 100}%")
print(f"Outras despesas item: R$ {outras_despesas_item}")
print()

# Cálculo correto: outras despesas por kg
outras_despesas_por_kg = outras_despesas_item / peso_compra
print(f"Outras despesas por kg: R$ {outras_despesas_por_kg}")

# Valor sem impostos (compra)
valor_sem_icms = valor_com_icms_compra * (1 - percentual_icms_compra)
valor_sem_impostos_base = valor_sem_icms * (1 - PIS_COFINS_PERCENTAGE)
valor_sem_impostos_compra = valor_sem_impostos_base + outras_despesas_por_kg

print(f"Valor sem ICMS: R$ {valor_sem_icms:.6f}")
print(f"Valor sem impostos (base): R$ {valor_sem_impostos_base:.6f}")
print(f"Valor sem impostos (com outras despesas): R$ {valor_sem_impostos_compra:.6f}")

# Total de compra
total_compra = peso_compra * valor_sem_impostos_compra
print(f"Total compra: R$ {total_compra:.2f}")

# Comparação com resultado da API
resultado_api = 1793.03
diferenca = abs(total_compra - resultado_api)

print()
print("=== COMPARAÇÃO ===")
print(f"Cálculo manual: R$ {total_compra:.2f}")
print(f"Resultado API: R$ {resultado_api}")
print(f"Diferença: R$ {diferenca:.2f}")

if diferenca < 0.01:
    print("✅ SUCESSO: Cálculo está correto!")
else:
    print("❌ ERRO: Ainda há diferença no cálculo")
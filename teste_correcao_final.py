#!/usr/bin/env python3
"""
Teste final para verificar se a correção do peso de venda para distribuição de frete funcionou
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.business_rules_calculator import BusinessRulesCalculator

# Payload do usuário (valores corretos)
payload = {
    "client_name": "CLIENTE TESTE",
    "freight_value_total": 500.0,
    "items": [
        {
            "product_name": "PRODUTO A",
            "peso_compra": 1000,
            "peso_venda": 1010,
            "valor_com_icms_compra": 2.11,
            "valor_com_icms_venda": 4.32,
            "percentual_icms_compra": 0.18,
            "percentual_icms_venda": 0.18,
            "outras_despesas_item": 0.0
        },
        {
            "product_name": "PRODUTO B",
            "peso_compra": 1000,
            "peso_venda": 1010,
            "valor_com_icms_compra": 2.11,
            "valor_com_icms_venda": 4.32,
            "percentual_icms_compra": 0.18,
            "percentual_icms_venda": 0.18,
            "outras_despesas_item": 0.0
        }
    ]
}

# Calcular usando peso de venda (CORRETO)
items_data = payload["items"]
soma_pesos_pedido_venda = sum(item.get('peso_venda', 0) for item in items_data)
outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in items_data)

print("=== TESTE FINAL - CORREÇÃO DO PESO DE VENDA ===")
print(f"Soma pesos pedido (usando peso_venda): {soma_pesos_pedido_venda} kg")
print(f"Frete total: R$ {payload['freight_value_total']:.2f}")
print(f"Frete por kg: R$ {payload['freight_value_total'] / soma_pesos_pedido_venda:.6f}")

# Calcular com BusinessRulesCalculator
calculator = BusinessRulesCalculator()
result = calculator.calculate_complete_budget(
    items_data=items_data,
    outras_despesas_totais=outras_despesas_totais,
    soma_pesos_pedido=soma_pesos_pedido_venda,
    freight_value_total=payload["freight_value_total"]
)

print("\n=== RESULTADOS CALCULADOS ===")
total_compra_calculado = result['totals']['soma_total_compra']
total_venda_calculado = result['totals']['soma_total_venda']

# Calcular rentabilidade manualmente se não estiver no resultado
if total_compra_calculado > 0:
    rentabilidade_calculada = ((total_venda_calculado - total_compra_calculado) / total_compra_calculado) * 100
else:
    rentabilidade_calculada = 0

print(f"Total compra: R$ {total_compra_calculado:.2f}")
print(f"Total venda: R$ {total_venda_calculado:.2f}")
print(f"Rentabilidade: {rentabilidade_calculada:.2f}%")

print("\n=== VALORES ESPERADOS PELO USUÁRIO ===")
print(f"Total compra esperado: R$ 3640.31")
print(f"Total venda esperado: R$ 6493.75")
print(f"Rentabilidade esperada: 78.38%")

print("\n=== DIFERENÇAS ===")
diff_compra = abs(total_compra_calculado - 3640.31)
diff_venda = abs(total_venda_calculado - 6493.75)
diff_rentabilidade = abs(rentabilidade_calculada - 78.38)

print(f"Diferença total compra: R$ {diff_compra:.2f}")
print(f"Diferença total venda: R$ {diff_venda:.2f}")
print(f"Diferença rentabilidade: {diff_rentabilidade:.2f} pontos percentuais")

# Verificar se está dentro da tolerância aceitável
tolerancia_valor = 5.0  # R$ 5,00
tolerancia_rentabilidade = 0.5  # 0.5 pontos percentuais

print("\n=== VALIDAÇÃO ===")
compra_ok = diff_compra <= tolerancia_valor
venda_ok = diff_venda <= tolerancia_valor
rentabilidade_ok = diff_rentabilidade <= tolerancia_rentabilidade

print(f"✅ Total compra OK: {compra_ok} (diferença: R$ {diff_compra:.2f})")
print(f"✅ Total venda OK: {venda_ok} (diferença: R$ {diff_venda:.2f})")
print(f"✅ Rentabilidade OK: {rentabilidade_ok} (diferença: {diff_rentabilidade:.2f}pp)")

if compra_ok and venda_ok and rentabilidade_ok:
    print("\n🎉 CORREÇÃO APLICADA COM SUCESSO!")
    print("Os valores calculados estão dentro da tolerância esperada.")
else:
    print("\n❌ AINDA HÁ DIFERENÇAS SIGNIFICATIVAS")
    print("Pode ser necessário investigar outros aspectos do cálculo.")

# Testar taxa de comissão
if 'commission_rate' in result:
    print(f"\n=== TAXA DE COMISSÃO ===")
    print(f"Taxa calculada: {result['commission_rate']:.2f}%")
    print(f"Taxa esperada: 4.00%")
    diff_comissao = abs(result['commission_rate'] - 4.0)
    comissao_ok = diff_comissao <= 0.1
    print(f"✅ Taxa de comissão OK: {comissao_ok} (diferença: {diff_comissao:.2f}pp)")
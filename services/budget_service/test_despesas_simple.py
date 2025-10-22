#!/usr/bin/env python3
"""
Teste simples para validar a correção das despesas
"""

import sys
sys.path.append('/app')

from app.services.budget_calculator import BudgetCalculatorService
from app.schemas.budget import BudgetItemSimplified

# Dados de teste da documentação
test_data = BudgetItemSimplified(
    description='Item de Teste',
    peso_compra=10.0,
    peso_venda=10.0,
    valor_com_icms_compra=100.0,
    percentual_icms_compra=0.18,
    outras_despesas_item=20.0,
    valor_com_icms_venda=120.0,
    percentual_icms_venda=0.17,
    percentual_ipi=0.0
)

print('🧪 Testando correção das despesas no cálculo de custos...')
print('=' * 60)
print(f'📊 Dados de entrada:')
print(f'   • Valor com ICMS (Compra): R$ {test_data.valor_com_icms_compra:.2f}')
print(f'   • ICMS (Compra): {test_data.percentual_icms_compra * 100:.0f}%')
print(f'   • Outras Despesas: R$ {test_data.outras_despesas_item:.2f}')
print(f'   • Peso: {test_data.peso_compra:.0f} kg')
print()

try:
    result = BudgetCalculatorService.calculate_simplified_item(test_data)
    valor_sem_impostos_compra = result.get('purchase_value_without_taxes', 0)
    
    print(f'✅ Resultado do cálculo:')
    print(f'   • Valor sem impostos (por kg): R$ {valor_sem_impostos_compra:.6f}')
    print(f'   • Valor total sem impostos: R$ {valor_sem_impostos_compra * test_data.peso_compra:.2f}')
    print()
    
    # Validação conforme documentação
    valor_esperado_por_kg = 76.415000
    valor_total_esperado = 764.15
    valor_total_calculado = valor_sem_impostos_compra * test_data.peso_compra
    
    print(f'🎯 Validação:')
    print(f'   • Valor esperado (por kg): R$ {valor_esperado_por_kg:.6f}')
    print(f'   • Valor calculado (por kg): R$ {valor_sem_impostos_compra:.6f}')
    print(f'   • Diferença (por kg): R$ {abs(valor_sem_impostos_compra - valor_esperado_por_kg):.6f}')
    print()
    print(f'   • Valor total esperado: R$ {valor_total_esperado:.2f}')
    print(f'   • Valor total calculado: R$ {valor_total_calculado:.2f}')
    print(f'   • Diferença total: R$ {abs(valor_total_calculado - valor_total_esperado):.2f}')
    print()
    
    tolerancia = 0.01
    if abs(valor_total_calculado - valor_total_esperado) <= tolerancia:
        print('✅ TESTE APROVADO: Cálculo das despesas está correto!')
        print('   As despesas estão sendo SOMADAS corretamente ao custo.')
        exit_code = 0
    else:
        print('❌ TESTE REPROVADO: Cálculo das despesas está incorreto!')
        print('   Verifique se as despesas estão sendo somadas (+) e não subtraídas (-).')
        exit_code = 1
        
except Exception as e:
    print(f'❌ ERRO no cálculo: {str(e)}')
    exit_code = 1

print('\n' + '=' * 60)
if exit_code == 0:
    print('🎉 VALIDAÇÃO CONCLUÍDA COM SUCESSO!')
else:
    print('⚠️  VALIDAÇÃO FALHOU!')

sys.exit(exit_code)
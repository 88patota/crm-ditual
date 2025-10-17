#!/usr/bin/env python3
"""
Teste para verificar se a correção do payment_condition está funcionando.
Este teste verifica se os campos estão sendo mapeados corretamente no código.
"""

import sys
import os

def test_payment_condition_fix():
    print("=== TESTE: CORREÇÃO DO PAYMENT_CONDITION ===")
    print()
    
    print("1. Verificando campos que deveriam estar mapeados:")
    print("   - payment_condition: Campo principal do problema")
    print("   - prazo_medio: Campo opcional também corrigido")
    print("   - outras_despesas_totais: Campo opcional também corrigido")
    print()
    
    # Verificar se o arquivo BudgetService tem os campos corretos no método create_budget
    print("2. Verificando se os campos estão sendo mapeados corretamente...")
    
    budget_service_path = '/Users/erikpatekoski/dev/crm-ditual/services/budget_service/app/services/budget_service.py'
    
    try:
        with open(budget_service_path, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"   ❌ Arquivo não encontrado: {budget_service_path}")
        return False
    
    fields_to_check = [
        'payment_condition=budget_data.payment_condition',
        'prazo_medio=budget_data.prazo_medio', 
        'outras_despesas_totais=budget_data.outras_despesas_totais'
    ]
    
    print("   Verificando mapeamento dos campos:")
    for field in fields_to_check:
        if field in source:
            print(f"   ✅ {field.split('=')[0]} - MAPEADO CORRETAMENTE")
        else:
            print(f"   ❌ {field.split('=')[0]} - FALTANDO NO MAPEAMENTO")
    
    print()
    print("3. Resultado:")
    
    all_mapped = all(field in source for field in fields_to_check)
    
    if all_mapped:
        print("   ✅ CORREÇÃO APLICADA COM SUCESSO!")
        print("   Todos os campos opcionais estão sendo mapeados corretamente.")
        print("   O payment_condition agora deve ser persistido no banco de dados.")
    else:
        print("   ❌ CORREÇÃO INCOMPLETA!")
        print("   Alguns campos ainda não estão sendo mapeados.")
    
    return all_mapped

if __name__ == "__main__":
    result = test_payment_condition_fix()
    sys.exit(0 if result else 1)
#!/usr/bin/env python3
"""
Teste para debugar problema de comissão no orçamento ID 79
Dados fornecidos:
- peso compra: 1000
- peso venda: 1050  
- valor_icms_compra: 6
- taxa: 18%
- peso_venda: 1050
- valor_icms_venda: 7
- taxa: 18%
- Comissão atual: 0.0 com valor de 294.00
- Comissão esperada: 73.50
"""

import sys
import os

# Adicionar o caminho do serviço de orçamentos
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator
from app.services.commission_service import CommissionService

def test_commission_calculation():
    """Teste com os dados exatos do orçamento ID 79"""
    
    print("=== TESTE DE COMISSÃO - ORÇAMENTO ID 79 ===")
    print()
    
    # Dados fornecidos pelo usuário
    item_data = {
        'description': 'Item Orçamento ID 79',
        'peso_compra': 1000,
        'peso_venda': 1050,  
        'valor_com_icms_compra': 6.0,  # R$ 6,00 por kg
        'percentual_icms_compra': 0.18,  # 18%
        'valor_com_icms_venda': 7.0,    # R$ 7,00 por kg
        'percentual_icms_venda': 0.18    # 18%
    }
    
    print("DADOS DE ENTRADA:")
    print(f"Peso Compra: {item_data['peso_compra']} kg")
    print(f"Peso Venda: {item_data['peso_venda']} kg")
    print(f"Valor Compra (com ICMS): R$ {item_data['valor_com_icms_compra']:.2f}/kg")
    print(f"ICMS Compra: {item_data['percentual_icms_compra']*100:.0f}%")
    print(f"Valor Venda (com ICMS): R$ {item_data['valor_com_icms_venda']:.2f}/kg")
    print(f"ICMS Venda: {item_data['percentual_icms_venda']*100:.0f}%")
    print()
    
    # Calcular usando as regras do sistema
    outras_despesas_totais = 0.0
    soma_pesos_pedido = item_data['peso_compra']
    
    try:
        resultado = BusinessRulesCalculator.calculate_complete_item(
            item_data, outras_despesas_totais, soma_pesos_pedido
        )
        
        print("=== CÁLCULOS INTERMEDIÁRIOS ===")
        print(f"Valor sem impostos compra: R$ {resultado['valor_sem_impostos_compra']:.6f}/kg")
        print(f"Valor sem impostos venda: R$ {resultado['valor_sem_impostos_venda']:.6f}/kg")
        print(f"Total compra (sem ICMS): R$ {resultado['total_compra_item']:.2f}")
        print(f"Total venda (sem ICMS): R$ {resultado['total_venda_item']:.2f}")
        print(f"Total compra (com ICMS): R$ {resultado['total_compra_item_com_icms']:.2f}")
        print(f"Total venda (com ICMS): R$ {resultado['total_venda_item_com_icms']:.2f}")
        print(f"Rentabilidade do item: {resultado['rentabilidade_item']*100:.2f}%")
        print()
        
        print("=== CÁLCULO DE COMISSÃO DO SISTEMA ===")
        print(f"Valor da comissão calculada: R$ {resultado['valor_comissao']:.2f}")
        print()
        
        # Vamos fazer o cálculo manual da comissão esperada
        print("=== CÁLCULO MANUAL ESPERADO ===")
        
        # Calcular valores sem impostos manualmente
        valor_sem_impostos_compra_manual = item_data['valor_com_icms_compra'] * (1 - item_data['percentual_icms_compra']) * (1 - 0.0925)
        valor_sem_impostos_venda_manual = item_data['valor_com_icms_venda'] * (1 - item_data['percentual_icms_venda']) * (1 - 0.0925)
        
        print(f"Valor sem impostos compra (manual): R$ {valor_sem_impostos_compra_manual:.6f}/kg")
        print(f"Valor sem impostos venda (manual): R$ {valor_sem_impostos_venda_manual:.6f}/kg")
        
        # Total compra e venda sem impostos
        total_compra_manual = item_data['peso_compra'] * valor_sem_impostos_compra_manual
        total_venda_manual = item_data['peso_venda'] * valor_sem_impostos_venda_manual
        
        print(f"Total compra (manual): R$ {total_compra_manual:.2f}")
        print(f"Total venda (manual): R$ {total_venda_manual:.2f}")
        
        # Rentabilidade manual (valores COM ICMS)
        total_compra_com_icms_manual = item_data['peso_compra'] * item_data['valor_com_icms_compra']
        total_venda_com_icms_manual = item_data['peso_venda'] * item_data['valor_com_icms_venda']
        rentabilidade_manual = (total_venda_com_icms_manual / total_compra_com_icms_manual) - 1
        
        print(f"Total compra com ICMS (manual): R$ {total_compra_com_icms_manual:.2f}")
        print(f"Total venda com ICMS (manual): R$ {total_venda_com_icms_manual:.2f}")
        print(f"Rentabilidade manual: {rentabilidade_manual*100:.2f}%")
        
        # Calcular comissão manual
        percentual_comissao = CommissionService.calculate_commission_percentage(rentabilidade_manual)
        comissao_manual = total_venda_com_icms_manual * percentual_comissao
        
        print(f"Percentual de comissão: {percentual_comissao*100:.2f}%")
        print(f"Comissão manual: R$ {comissao_manual:.2f}")
        print()
        
        # Teste da nova regra de comissão com ajuste de quantidade
        print("=== TESTE NOVA REGRA DE COMISSÃO ===")
        comissao_nova_regra = CommissionService.calculate_commission_value_with_quantity_adjustment(
            resultado['total_venda_item_com_icms'],
            resultado['total_compra_item'],
            item_data['peso_venda'],
            item_data['peso_compra'],
            resultado['valor_sem_impostos_venda'],
            resultado['valor_sem_impostos_compra']
        )
        print(f"Comissão nova regra: R$ {comissao_nova_regra:.2f}")
        print()
        
        # Verificar faixas de comissão
        print("=== FAIXAS DE COMISSÃO ===")
        for bracket in CommissionService.COMMISSION_BRACKETS:
            min_perc = bracket["min_profitability"] * 100
            max_perc = bracket["max_profitability"] * 100 if bracket["max_profitability"] != float('inf') else "∞"
            comm_perc = bracket["commission_rate"] * 100
            
            if rentabilidade_manual >= bracket["min_profitability"] and rentabilidade_manual < bracket["max_profitability"]:
                print(f">>> FAIXA APLICADA: {min_perc:.0f}% - {max_perc}% → {comm_perc:.1f}% comissão")
            else:
                print(f"    Faixa: {min_perc:.0f}% - {max_perc}% → {comm_perc:.1f}% comissão")
        
        print()
        print("=== ANÁLISE DE DIFERENÇAS ===")
        print(f"Comissão sistema atual: R$ {resultado['valor_comissao']:.2f}")
        print(f"Comissão esperada (manual): R$ {comissao_manual:.2f}")
        print(f"Comissão nova regra: R$ {comissao_nova_regra:.2f}")
        print(f"Comissão esperada pelo usuário: R$ 73.50")
        print(f"Valor mencionado pelo usuário: R$ 294.00")
        print()
        
        diferenca_esperada = abs(comissao_manual - 73.50)
        print(f"Diferença entre cálculo manual e esperado: R$ {diferenca_esperada:.2f}")
        
        # Tentar descobrir de onde vem o valor 294.00
        print(f"Possível origem do 294.00:")
        print(f"- Total venda com ICMS: R$ {total_venda_com_icms_manual:.2f}")
        print(f"- Total venda sem ICMS: R$ {total_venda_manual:.2f}")
        print(f"- Diferença de peso * valor unitário: {(item_data['peso_venda'] - item_data['peso_compra']) * item_data['valor_com_icms_venda']}")
        
    except Exception as e:
        print(f"ERRO no cálculo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_commission_calculation()
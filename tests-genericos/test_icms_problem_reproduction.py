#!/usr/bin/env python3
"""
Teste para reproduzir o problema do ICMS sendo forçado para 18%
"""

import sys
import os

# Adicionar o caminho do serviço de orçamentos
sys.path.append('/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

from app.services.business_rules_calculator import BusinessRulesCalculator

def test_icms_different_values():
    """Teste com valores de ICMS diferentes de 18%"""
    
    print("=== TESTE PROBLEMA ICMS DIFERENTE DE 18% ===")
    print()
    
    # Caso 1: ICMS de compra = 12%, ICMS de venda = 7%
    item_data_caso1 = {
        'description': 'Teste ICMS 12% e 7%',
        'peso_compra': 1000,
        'peso_venda': 1000,  
        'valor_com_icms_compra': 10.0,
        'percentual_icms_compra': 0.12,  # 12%
        'valor_com_icms_venda': 15.0,
        'percentual_icms_venda': 0.07    # 7%
    }
    
    print("CASO 1 - ICMS Compra: 12%, ICMS Venda: 7%")
    print(f"Valor compra com ICMS: R$ {item_data_caso1['valor_com_icms_compra']:.2f}")
    print(f"ICMS compra enviado: {item_data_caso1['percentual_icms_compra']*100:.0f}%")
    print(f"Valor venda com ICMS: R$ {item_data_caso1['valor_com_icms_venda']:.2f}")
    print(f"ICMS venda enviado: {item_data_caso1['percentual_icms_venda']*100:.0f}%")
    print()
    
    # Calcular manualmente o que DEVERIA ser
    valor_sem_icms_compra_esperado = item_data_caso1['valor_com_icms_compra'] * (1 - 0.12) * (1 - 0.0925)
    valor_sem_icms_venda_esperado = item_data_caso1['valor_com_icms_venda'] * (1 - 0.07) * (1 - 0.0925)
    
    print("VALORES ESPERADOS (com ICMS correto):")
    print(f"Valor sem impostos compra: R$ {valor_sem_icms_compra_esperado:.6f}")
    print(f"Valor sem impostos venda: R$ {valor_sem_icms_venda_esperado:.6f}")
    print()
    
    # Calcular usando o sistema atual
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 1000
    
    try:
        resultado = BusinessRulesCalculator.calculate_complete_item(
            item_data_caso1, outras_despesas_totais, soma_pesos_pedido
        )
        
        print("VALORES CALCULADOS PELO SISTEMA:")
        print(f"ICMS compra usado: {resultado['percentual_icms_compra']*100:.0f}%")
        print(f"ICMS venda usado: {resultado['percentual_icms_venda']*100:.0f}%")
        print(f"Valor sem impostos compra: R$ {resultado['valor_sem_impostos_compra']:.6f}")
        print(f"Valor sem impostos venda: R$ {resultado['valor_sem_impostos_venda']:.6f}")
        print()
        
        # Verificar se está usando os valores corretos
        icms_compra_correto = abs(resultado['percentual_icms_compra'] - item_data_caso1['percentual_icms_compra']) < 0.001
        icms_venda_correto = abs(resultado['percentual_icms_venda'] - item_data_caso1['percentual_icms_venda']) < 0.001
        
        if icms_compra_correto and icms_venda_correto:
            print("✅ ICMS sendo usado corretamente!")
        else:
            print("❌ PROBLEMA: ICMS não está sendo usado corretamente!")
            print(f"   ICMS compra: esperado {item_data_caso1['percentual_icms_compra']*100:.0f}%, usado {resultado['percentual_icms_compra']*100:.0f}%")
            print(f"   ICMS venda: esperado {item_data_caso1['percentual_icms_venda']*100:.0f}%, usado {resultado['percentual_icms_venda']*100:.0f}%")
        
        print()
        
    except Exception as e:
        print(f"ERRO no cálculo: {e}")
        import traceback
        traceback.print_exc()

def test_icms_missing_fields():
    """Teste quando campos de ICMS estão faltando"""
    
    print("=== TESTE CAMPOS ICMS FALTANDO ===")
    print()
    
    # Caso onde os campos de ICMS não existem no dicionário
    item_data_sem_icms = {
        'description': 'Teste sem campos ICMS',
        'peso_compra': 1000,
        'peso_venda': 1000,  
        'valor_com_icms_compra': 10.0,
        'valor_com_icms_venda': 15.0,
        # Campos de ICMS intencionalmente omitidos
    }
    
    print("DADOS SEM CAMPOS ICMS:")
    print("percentual_icms_compra: CAMPO FALTANDO")
    print("percentual_icms_venda: CAMPO FALTANDO")
    print()
    
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 1000
    
    try:
        resultado = BusinessRulesCalculator.calculate_complete_item(
            item_data_sem_icms, outras_despesas_totais, soma_pesos_pedido
        )
        
        print("VALORES USADOS PELO SISTEMA:")
        print(f"ICMS compra padrão: {resultado['percentual_icms_compra']*100:.0f}%")
        print(f"ICMS venda padrão: {resultado['percentual_icms_venda']*100:.0f}%")
        print()
        
        if resultado['percentual_icms_compra'] == 0.18 and resultado['percentual_icms_venda'] == 0.18:
            print("✅ Sistema usando padrão de 18% quando campos estão faltando (comportamento esperado)")
        else:
            print("❌ Sistema não está usando padrão correto")
        
    except Exception as e:
        print(f"ERRO no cálculo: {e}")

def test_icms_zero_values():
    """Teste com valores de ICMS zero"""
    
    print("=== TESTE ICMS ZERO ===")
    print()
    
    item_data_icms_zero = {
        'description': 'Teste ICMS 0%',
        'peso_compra': 1000,
        'peso_venda': 1000,  
        'valor_com_icms_compra': 10.0,
        'percentual_icms_compra': 0.0,  # 0%
        'valor_com_icms_venda': 15.0,
        'percentual_icms_venda': 0.0    # 0%
    }
    
    print("DADOS COM ICMS 0%:")
    print(f"ICMS compra: {item_data_icms_zero['percentual_icms_compra']*100:.0f}%")
    print(f"ICMS venda: {item_data_icms_zero['percentual_icms_venda']*100:.0f}%")
    print()
    
    outras_despesas_totais = 0.0
    soma_pesos_pedido = 1000
    
    try:
        resultado = BusinessRulesCalculator.calculate_complete_item(
            item_data_icms_zero, outras_despesas_totais, soma_pesos_pedido
        )
        
        print("VALORES USADOS PELO SISTEMA:")
        print(f"ICMS compra usado: {resultado['percentual_icms_compra']*100:.0f}%")
        print(f"ICMS venda usado: {resultado['percentual_icms_venda']*100:.0f}%")
        print()
        
        # Com ICMS 0%, valores sem ICMS deveriam ser apenas descontados PIS/COFINS
        valor_esperado_compra = 10.0 * (1 - 0.0925)  # Só PIS/COFINS
        valor_esperado_venda = 15.0 * (1 - 0.0925)   # Só PIS/COFINS
        
        print(f"Valor sem impostos compra esperado: R$ {valor_esperado_compra:.6f}")
        print(f"Valor sem impostos compra calculado: R$ {resultado['valor_sem_impostos_compra']:.6f}")
        print(f"Valor sem impostos venda esperado: R$ {valor_esperado_venda:.6f}")  
        print(f"Valor sem impostos venda calculado: R$ {resultado['valor_sem_impostos_venda']:.6f}")
        
        if (abs(resultado['valor_sem_impostos_compra'] - valor_esperado_compra) < 0.01 and
            abs(resultado['valor_sem_impostos_venda'] - valor_esperado_venda) < 0.01):
            print("✅ Cálculo com ICMS 0% correto!")
        else:
            print("❌ Cálculo com ICMS 0% incorreto!")
        
    except Exception as e:
        print(f"ERRO no cálculo: {e}")

if __name__ == "__main__":
    test_icms_different_values()
    test_icms_missing_fields() 
    test_icms_zero_values()
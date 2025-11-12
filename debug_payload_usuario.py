#!/usr/bin/env python3
"""
Debug da discrepância entre os totais informados pelo usuário e os calculados
"""

def debug_payload_usuario():
    """Debug detalhado do payload do usuário"""
    
    # Payload fornecido pelo usuário
    payload = {
        "total_purchase_value": 3640.314,
        "total_sale_value": 6493.75056,
        "profitability_percentage": 0.7838435255859797,
        "items": [
            {
                "peso_compra": 1000,
                "peso_venda": 1010,
                "valor_com_icms_compra": 2.11,
                "valor_com_icms_venda": 4.32,
            },
            {
                "peso_compra": 1000,
                "peso_venda": 1010,
                "valor_com_icms_compra": 2.11,
                "valor_com_icms_venda": 4.32,
            }
        ]
    }
    
    print("=== DEBUG PAYLOAD USUÁRIO ===")
    print(f"Total compra informado: R$ {payload['total_purchase_value']:.2f}")
    print(f"Total venda informado: R$ {payload['total_sale_value']:.2f}")
    print(f"Rentabilidade informada: {payload['profitability_percentage']:.4f} = {payload['profitability_percentage']*100:.2f}%")
    
    print("\n=== CÁLCULO DIRETO DOS ITENS ===")
    total_compra_calculado = 0
    total_venda_calculado = 0
    
    for i, item in enumerate(payload['items'], 1):
        compra_item = item['peso_compra'] * item['valor_com_icms_compra']
        venda_item = item['peso_venda'] * item['valor_com_icms_venda']
        
        print(f"Item {i}:")
        print(f"  Compra: {item['peso_compra']} × {item['valor_com_icms_compra']} = R$ {compra_item:.2f}")
        print(f"  Venda: {item['peso_venda']} × {item['valor_com_icms_venda']} = R$ {venda_item:.2f}")
        
        total_compra_calculado += compra_item
        total_venda_calculado += venda_item
    
    print(f"\nTotais calculados:")
    print(f"  Total compra: R$ {total_compra_calculado:.2f}")
    print(f"  Total venda: R$ {total_venda_calculado:.2f}")
    
    rentabilidade_calculada = ((total_venda_calculado - total_compra_calculado) / total_compra_calculado) * 100
    print(f"  Rentabilidade: {rentabilidade_calculada:.2f}%")
    
    print("\n=== DISCREPÂNCIAS ===")
    diff_compra = payload['total_purchase_value'] - total_compra_calculado
    diff_venda = payload['total_sale_value'] - total_venda_calculado
    diff_rentabilidade = (payload['profitability_percentage'] * 100) - rentabilidade_calculada
    
    print(f"Diferença compra: R$ {diff_compra:.2f}")
    print(f"Diferença venda: R$ {diff_venda:.2f}")
    print(f"Diferença rentabilidade: {diff_rentabilidade:.2f} pontos percentuais")
    
    print("\n=== ANÁLISE ===")
    if abs(diff_compra) > 0.01 or abs(diff_venda) > 0.01:
        print("❌ Os totais informados NÃO batem com os itens!")
        print("Possíveis causas:")
        print("1. Os itens não representam o orçamento completo")
        print("2. Há outras despesas ou fretes não informados")
        print("3. Os valores unitários foram alterados")
        print("4. Há diferença na base de cálculo (COM vs SEM impostos)")
        
        # Tentar descobrir qual seria o valor unitário correto
        print("\n=== TENTATIVA DE CORREÇÃO ===")
        
        # Se assumirmos que os pesos estão corretos, qual seria o valor unitário?
        peso_total_compra = sum(item['peso_compra'] for item in payload['items'])
        peso_total_venda = sum(item['peso_venda'] for item in payload['items'])
        
        valor_unitario_compra_correto = payload['total_purchase_value'] / peso_total_compra
        valor_unitario_venda_correto = payload['total_sale_value'] / peso_total_venda
        
        print(f"Valor unitário compra que resultaria no total: R$ {valor_unitario_compra_correto:.6f}")
        print(f"Valor unitário venda que resultaria no total: R$ {valor_unitario_venda_correto:.6f}")
        print(f"Valor informado compra: R$ {payload['items'][0]['valor_com_icms_compra']:.6f}")
        print(f"Valor informado venda: R$ {payload['items'][0]['valor_com_icms_venda']:.6f}")
        
        # Verificar se a diferença pode ser explicada por impostos
        print("\n=== ANÁLISE DE IMPOSTOS ===")
        # Se os valores informados são COM ICMS e os totais são SEM ICMS
        icms_compra = 0.18  # 18%
        icms_venda = 0.18   # 18%
        
        valor_sem_icms_compra = payload['items'][0]['valor_com_icms_compra'] / (1 + icms_compra)
        valor_sem_icms_venda = payload['items'][0]['valor_com_icms_venda'] / (1 + icms_venda)
        
        total_sem_icms_compra = peso_total_compra * valor_sem_icms_compra
        total_sem_icms_venda = peso_total_venda * valor_sem_icms_venda
        
        print(f"Se os totais fossem SEM ICMS:")
        print(f"  Total compra SEM ICMS: R$ {total_sem_icms_compra:.2f}")
        print(f"  Total venda SEM ICMS: R$ {total_sem_icms_venda:.2f}")
        print(f"  Diferença com total informado compra: R$ {abs(payload['total_purchase_value'] - total_sem_icms_compra):.2f}")
        print(f"  Diferença com total informado venda: R$ {abs(payload['total_sale_value'] - total_sem_icms_venda):.2f}")
        
        if abs(payload['total_purchase_value'] - total_sem_icms_compra) < 1.0:
            print("✅ POSSÍVEL CAUSA: Os totais são SEM ICMS, mas os valores unitários são COM ICMS!")
    else:
        print("✅ Os totais batem com os itens")

if __name__ == "__main__":
    debug_payload_usuario()
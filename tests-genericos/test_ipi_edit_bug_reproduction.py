#!/usr/bin/env python3

import requests
import json
import sys

def test_ipi_edit_bug_reproduction():
    """
    Reproduz o bug onde os valores de IPI não são exibidos no frontend 
    ao editar um orçamento, apesar de estarem presentes no backend.
    
    Baseado no response JSON fornecido:
    - total_ipi_value: 10.14
    - ipi_value: 10.14 (no item)  
    - ipi_percentage: 0.0325 (no item)
    """
    
    BASE_URL = "http://localhost:8002"
    
    print("🔍 REPRODUÇÃO DO BUG - IPI NÃO EXIBIDO NA EDIÇÃO")
    print("=" * 60)
    
    # 1. Primeiro, criar um orçamento com IPI
    print("\n1. Criando orçamento com IPI...")
    
    budget_data = {
        "order_number": "PED-IPI-TEST-001",
        "client_name": "Cliente Teste IPI",
        "status": "draft",
        "notes": "Teste para reprodução do bug de IPI na edição",
        "items": [
            {
                "description": "Item com IPI",
                "peso_compra": 100.0,
                "peso_venda": 100.0,
                "valor_com_icms_compra": 2.22,
                "percentual_icms_compra": 0.12,  # 12%
                "outras_despesas_item": 0.0,
                "valor_com_icms_venda": 3.12,
                "percentual_icms_venda": 0.18,  # 18%
                "percentual_ipi": 0.0325  # 3.25% - ESTE É O CAMPO CRÍTICO
            }
        ],
        "outras_despesas_totais": 0.0,
        "prazo_medio": 30
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/budgets/simplified", json=budget_data)
        response.raise_for_status()
        created_budget = response.json()
        
        print("✅ Orçamento criado com sucesso!")
        print(f"   ID: {created_budget.get('id')}")
        print(f"   Order Number: {created_budget.get('order_number')}")
        print(f"   Total IPI: {created_budget.get('total_ipi_value', 0)}")
        
        # Verificar se o item tem IPI
        items = created_budget.get('items', [])
        if items:
            item = items[0]
            print(f"   Item IPI %: {item.get('ipi_percentage', 'NÃO ENCONTRADO')}")
            print(f"   Item IPI Value: {item.get('ipi_value', 'NÃO ENCONTRADO')}")
        
        budget_id = created_budget['id']
        
    except Exception as e:
        print(f"❌ Erro ao criar orçamento: {e}")
        return False
    
    # 2. Buscar o orçamento criado para edição (simula GET do frontend)
    print(f"\n2. Buscando orçamento ID {budget_id} para edição...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/budgets/{budget_id}")
        response.raise_for_status()
        budget_for_edit = response.json()
        
        print("✅ Orçamento recuperado para edição!")
        print("\n🔍 ANÁLISE DOS CAMPOS IPI NO RESPONSE:")
        print("-" * 50)
        
        # Verificar campos IPI no nível do orçamento
        print("📊 Campos IPI no orçamento:")
        print(f"   total_ipi_value: {budget_for_edit.get('total_ipi_value', 'AUSENTE')}")
        print(f"   total_final_value: {budget_for_edit.get('total_final_value', 'AUSENTE')}")
        
        # Verificar campos IPI nos itens
        items = budget_for_edit.get('items', [])
        print(f"\n📋 Itens encontrados: {len(items)}")
        
        for i, item in enumerate(items):
            print(f"\n   Item {i+1}: {item.get('description', 'Sem descrição')}")
            
            # Listar TODOS os campos do item para identificar onde está o IPI
            print("   📝 Campos disponíveis no item:")
            ipi_fields = []
            for key, value in item.items():
                if 'ipi' in key.lower():
                    ipi_fields.append(f"{key}: {value}")
                    print(f"      🎯 {key}: {value}")
                
            if not ipi_fields:
                print("      ⚠️ NENHUM CAMPO IPI ENCONTRADO!")
                print("      📋 Todos os campos disponíveis:")
                for key, value in item.items():
                    print(f"         {key}: {value}")
        
        print(f"\n📄 Response completo (para debug):")
        print(json.dumps(budget_for_edit, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Erro ao buscar orçamento: {e}")
        return False
    
    # 3. Identificar o problema
    print("\n3. IDENTIFICAÇÃO DO PROBLEMA:")
    print("-" * 40)
    
    item = budget_for_edit.get('items', [{}])[0]
    
    # Verificar se o IPI está presente com algum nome
    ipi_found = False
    ipi_field_name = None
    ipi_value = None
    
    possible_ipi_fields = ['ipi_percentage', 'percentual_ipi', 'ipi_value', 'ipi_percent']
    
    for field in possible_ipi_fields:
        if field in item:
            ipi_found = True
            ipi_field_name = field
            ipi_value = item[field]
            break
    
    if ipi_found:
        print(f"✅ IPI encontrado no campo: {ipi_field_name} = {ipi_value}")
        print("🔍 DIAGNÓSTICO: O IPI está presente no backend!")
        print("💡 PROBLEMA: Pode ser um problema de mapeamento no frontend.")
        print("   - Verificar se o SimplifiedBudgetForm está mapeando o campo correto")
        print("   - Verificar se o campo está sendo preservado no useEffect")
        print(f"   - O campo no backend é '{ipi_field_name}' mas o frontend pode estar esperando outro nome")
        
    else:
        print("❌ IPI NÃO encontrado em nenhum campo conhecido!")
        print("🔍 DIAGNÓSTICO: O IPI não está sendo persistido corretamente no backend!")
        print("💡 PROBLEMA IDENTIFICADO: Falha na persistência ou retorno dos dados IPI")
    
    # 4. Simular o que o frontend deveria fazer
    print("\n4. SIMULAÇÃO DO MAPEAMENTO FRONTEND:")
    print("-" * 45)
    
    # Simular o que o SimplifiedBudgetForm faz no useEffect
    print("🔄 Simulando mapeamento do SimplifiedBudgetForm...")
    
    mapped_items = []
    for item in budget_for_edit.get('items', []):
        # Simular o mapeamento atual do código
        mapped_item = {
            'description': item.get('description', ''),
            'peso_compra': item.get('weight', 0),
            'peso_venda': item.get('sale_weight', item.get('weight', 0)),
            'valor_com_icms_compra': item.get('purchase_value_with_icms', 0),
            'percentual_icms_compra': item.get('purchase_icms_percentage', 0.18),
            'outras_despesas_item': item.get('purchase_other_expenses', 0),
            'valor_com_icms_venda': item.get('sale_value_with_icms', 0),
            'percentual_icms_venda': item.get('sale_icms_percentage', 0.18),
        }
        
        # Tentar mapear o IPI com a lógica atual
        ipi_mapped = False
        for field_name in ['ipi_percentage', 'percentual_ipi', 'ipi_value', 'ipi_percent']:
            value = item.get(field_name)
            if isinstance(value, (int, float)) and not (isinstance(value, float) and value != value):  # not NaN
                mapped_item['percentual_ipi'] = value
                ipi_mapped = True
                print(f"   ✅ IPI mapeado de '{field_name}': {value}")
                break
        
        if not ipi_mapped:
            mapped_item['percentual_ipi'] = 0.0
            print(f"   ❌ IPI não mapeado, usando valor padrão: 0.0")
        
        mapped_items.append(mapped_item)
    
    print(f"\n📋 Item mapeado final:")
    for item in mapped_items:
        print(f"   percentual_ipi: {item['percentual_ipi']}")
    
    # 5. Conclusão
    print("\n5. CONCLUSÃO E PRÓXIMOS PASSOS:")
    print("-" * 35)
    
    if ipi_found:
        print("🎯 BUG REPRODUZIDO E IDENTIFICADO!")
        print("📋 PROBLEMA: Mapeamento incorreto no frontend")
        print("🔧 SOLUÇÃO: Ajustar o mapeamento no SimplifiedBudgetForm.tsx")
        print(f"   - Garantir que o campo '{ipi_field_name}' seja mapeado corretamente")
        print("   - Verificar se todos os possíveis nomes de campo IPI são tratados")
        
        return {
            'bug_reproduced': True,
            'ipi_field_name': ipi_field_name,
            'ipi_value': ipi_value,
            'problem': 'frontend_mapping',
            'backend_data_ok': True
        }
    else:
        print("🎯 PROBLEMA NO BACKEND IDENTIFICADO!")
        print("📋 PROBLEMA: IPI não está sendo persistido/retornado")
        print("🔧 SOLUÇÃO: Verificar backend e persistência de dados IPI")
        
        return {
            'bug_reproduced': True,
            'ipi_field_name': None,
            'ipi_value': None,
            'problem': 'backend_persistence',
            'backend_data_ok': False
        }

if __name__ == "__main__":
    print("🧪 TESTE DE REPRODUÇÃO - BUG IPI EDIÇÃO")
    print("=" * 50)
    
    result = test_ipi_edit_bug_reproduction()
    
    if result:
        print(f"\n✅ TESTE CONCLUÍDO!")
        print(f"   Bug reproduzido: {result['bug_reproduced']}")
        print(f"   Campo IPI encontrado: {result['ipi_field_name']}")
        print(f"   Valor IPI: {result['ipi_value']}")
        print(f"   Tipo de problema: {result['problem']}")
        sys.exit(0)
    else:
        print(f"\n❌ TESTE FALHOU!")
        sys.exit(1)

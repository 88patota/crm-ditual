#!/usr/bin/env python3

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

async def test_ipi_edit_value_bug():
    """
    Reproduz o bug específico reportado: 
    o valor do IPI ao editar não está sendo exibido corretamente (mostra 0 ao invés do valor salvo)
    """
    base_url = "http://localhost:8000"
    
    # Dados de login
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    
    async with aiohttp.ClientSession() as session:
        print("=== TESTE IPI EDIT BUG REPRODUCTION ===")
        
        # 1. Login
        print("\n1. Fazendo login...")
        async with session.post(f"{base_url}/auth/login", json=login_data) as response:
            if response.status != 200:
                print(f"❌ Erro no login: {response.status}")
                text = await response.text()
                print(f"Response: {text}")
                return
            
            login_response = await response.json()
            token = login_response["access_token"]
            print(f"✅ Login successful. Token: {token[:50]}...")
        
        # Headers com token
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Criar orçamento com IPI não-zero
        print("\n2. Criando orçamento com IPI não-zero (3.25%)...")
        budget_data = {
            "order_number": f"TEST-IPI-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "client_name": "Cliente Teste IPI",
            "status": "draft",
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "notes": "Teste de bug do IPI na edição",
            "items": [
                {
                    "description": "Produto com IPI 3.25%",
                    "peso_compra": 100.0,
                    "peso_venda": 95.0,
                    "valor_com_icms_compra": 1000.0,
                    "percentual_icms_compra": 0.18,
                    "outras_despesas_item": 0.0,
                    "valor_com_icms_venda": 1300.0,
                    "percentual_icms_venda": 0.18,
                    "percentual_ipi": 0.0325  # 3.25% - VALOR NÃO-ZERO
                }
            ]
        }
        
        async with session.post(f"{base_url}/budgets/simplified", json=budget_data, headers=headers) as response:
            if response.status != 201:
                print(f"❌ Erro ao criar orçamento: {response.status}")
                text = await response.text()
                print(f"Response: {text}")
                return
            
            created_budget = await response.json()
            budget_id = created_budget["id"]
            order_number = created_budget["order_number"]
            
            print(f"✅ Orçamento criado: ID {budget_id}, Order: {order_number}")
            
            # Verificar se IPI foi salvo corretamente
            if created_budget["items"]:
                saved_ipi = created_budget["items"][0].get("ipi_percentage")
                print(f"   📊 IPI salvo no banco: {saved_ipi}")
                print(f"   📊 IPI esperado: 0.0325")
                
                if abs(float(saved_ipi or 0) - 0.0325) < 0.0001:
                    print(f"   ✅ IPI salvo corretamente!")
                else:
                    print(f"   ❌ IPI NÃO foi salvo corretamente!")
        
        # 3. Buscar o orçamento para edição (simulando o que o frontend faz)
        print(f"\n3. Buscando orçamento {budget_id} para edição...")
        async with session.get(f"{base_url}/budgets/{budget_id}", headers=headers) as response:
            if response.status != 200:
                print(f"❌ Erro ao buscar orçamento: {response.status}")
                text = await response.text()
                print(f"Response: {text}")
                return
            
            retrieved_budget = await response.json()
            print(f"✅ Orçamento encontrado")
            
            # Analisar os dados como chegam do backend
            if retrieved_budget["items"]:
                item = retrieved_budget["items"][0]
                ipi_from_backend = item.get("ipi_percentage")
                
                print(f"\n=== ANÁLISE DOS DADOS DO BACKEND ===")
                print(f"📋 Descrição: {item.get('description')}")
                print(f"📋 IPI Percentage: {ipi_from_backend}")
                print(f"📋 IPI Value: {item.get('ipi_value')}")
                print(f"📋 Tipo do IPI: {type(ipi_from_backend)}")
                
                # Verificar se o problema está no backend ou frontend
                if ipi_from_backend is None:
                    print(f"❌ PROBLEMA ENCONTRADO: Backend retorna ipi_percentage = None")
                elif float(ipi_from_backend) == 0.0:
                    print(f"❌ PROBLEMA ENCONTRADO: Backend retorna ipi_percentage = 0.0 (perdeu o valor)")
                elif abs(float(ipi_from_backend) - 0.0325) < 0.0001:
                    print(f"✅ Backend retorna IPI correto: {ipi_from_backend}")
                    print(f"   ⚠️  Problema pode estar no FRONTEND!")
                else:
                    print(f"⚠️  Backend retorna IPI inesperado: {ipi_from_backend}")
                
                # Simular processamento do frontend (como no SimplifiedBudgetForm)
                print(f"\n=== SIMULAÇÃO DO PROCESSAMENTO FRONTEND ===")
                
                # Dados iniciais como chegam do backend
                initial_data_items = [{"desc": item.get('description'), "ipi_original": item.get('ipi_percentage')}]
                print(f"Initial data items: {initial_data_items}")
                
                # Processamento como feito no SimplifiedBudgetForm
                processed_item = {
                    **item,
                    # O problema pode estar aqui - verificar se o valor é preservado
                    'percentual_ipi': item.get('ipi_percentage') if isinstance(item.get('ipi_percentage'), (int, float)) else 0.0
                }
                
                processed_items = [{"desc": processed_item.get('description'), "ipi_processed": processed_item.get('percentual_ipi')}]
                print(f"Items after processing: {processed_items}")
                
                # Verificar se o processamento preserva o valor
                original_ipi = item.get('ipi_percentage')
                processed_ipi = processed_item.get('percentual_ipi')
                
                if original_ipi is not None and processed_ipi is not None:
                    if abs(float(original_ipi) - float(processed_ipi)) < 0.0001:
                        print(f"✅ Processamento frontend preserva o valor IPI")
                    else:
                        print(f"❌ PROBLEMA: Processamento frontend perde o valor IPI!")
                        print(f"   Original: {original_ipi} -> Processado: {processed_ipi}")
                else:
                    print(f"❌ PROBLEMA: Um dos valores é None!")
                    print(f"   Original: {original_ipi} -> Processado: {processed_ipi}")
        
        # 4. Testar o endpoint de busca por order number (usado pelo frontend)
        print(f"\n4. Testando busca por order number (como usado pelo frontend)...")
        async with session.get(f"{base_url}/budgets/order/{order_number}", headers=headers) as response:
            if response.status != 200:
                print(f"❌ Erro ao buscar por order number: {response.status}")
                text = await response.text()
                print(f"Response: {text}")
                return
            
            budget_by_order = await response.json()
            
            if budget_by_order["items"]:
                item = budget_by_order["items"][0]
                ipi_by_order = item.get("ipi_percentage")
                
                print(f"📋 IPI via order number: {ipi_by_order}")
                
                if ipi_by_order is not None and abs(float(ipi_by_order) - 0.0325) < 0.0001:
                    print(f"✅ Busca por order number retorna IPI correto")
                else:
                    print(f"❌ Busca por order number tem problema com IPI")
        
        print(f"\n=== DIAGNÓSTICO FINAL ===")
        print(f"Se o backend retorna o IPI correto mas o frontend mostra 0:")
        print(f"  - O problema está na conversão/mapeamento dos dados no frontend")
        print(f"  - Verificar SimplifiedBudgetForm.tsx linha ~89-91 (processamento inicial)")
        print(f"  - Verificar se os nomes dos campos estão corretos")
        print(f"  - Verificar se o tipo de dados está sendo preservado")
        
        print(f"\nSe o backend já retorna IPI = 0 ou None:")
        print(f"  - O problema está no salvamento/recuperação do banco de dados")
        print(f"  - Verificar BudgetService.get_budget_by_id()")
        print(f"  - Verificar se o campo ipi_percentage está sendo mapeado corretamente")

if __name__ == "__main__":
    asyncio.run(test_ipi_edit_value_bug())

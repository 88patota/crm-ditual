#!/usr/bin/env python3
"""
Teste para validar se o campo PRAZO (delivery_time) está sendo corretamente
enviado e salvo ao criar um novo orçamento usando o endpoint simplificado.

Este teste verifica:
1. Se o campo delivery_time é enviado corretamente no payload
2. Se o campo é salvo no banco de dados
3. Se o campo é retornado corretamente na consulta
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# Configuração do teste
BASE_URL_GATEWAY = "http://localhost:8000"
BASE_URL_USER = "http://localhost:8001"
BASE_URL_BUDGET = "http://localhost:8002"
TEST_USER = {
    "username": "admin",
    "password": "admin123"
}

async def get_auth_token():
    """Obter token de autenticação"""
    async with aiohttp.ClientSession() as session:
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        
        async with session.post(f"{BASE_URL_USER}/api/v1/users/login", 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(login_data)) as response:
            if response.status == 200:
                result = await response.json()
                return result["access_token"]
            else:
                raise Exception(f"Falha no login: {response.status}")

async def test_prazo_field_creation():
    """Teste principal: criar orçamento com campo PRAZO e verificar se é salvo"""
    
    print("🔍 TESTE: Validação do campo PRAZO (delivery_time)")
    print("=" * 60)
    
    try:
        # 1. Obter token de autenticação
        print("1. Obtendo token de autenticação...")
        token = await get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Preparar dados do orçamento com valores de PRAZO específicos
        budget_data = {
            "client_name": "Cliente Teste PRAZO",
            "status": "draft",
            "notes": "Teste do campo delivery_time",
            "items": [
                {
                    "description": "Item 1 - Prazo 15 dias",
                    "peso_compra": 10.0,
                    "valor_com_icms_compra": 100.0,
                    "percentual_icms_compra": 0.17,
                    "outras_despesas_item": 5.0,
                    "peso_venda": 10.0,
                    "valor_com_icms_venda": 150.0,
                    "percentual_icms_venda": 0.17,
                    "percentual_ipi": 0.0,
                    "delivery_time": "15"  # CAMPO PRAZO - 15 dias
                },
                {
                    "description": "Item 2 - Prazo 30 dias",
                    "peso_compra": 5.0,
                    "valor_com_icms_compra": 50.0,
                    "percentual_icms_compra": 0.17,
                    "outras_despesas_item": 2.0,
                    "peso_venda": 5.0,
                    "valor_com_icms_venda": 80.0,
                    "percentual_icms_venda": 0.17,
                    "percentual_ipi": 0.0325,
                    "delivery_time": "30"  # CAMPO PRAZO - 30 dias
                },
                {
                    "description": "Item 3 - Prazo imediato",
                    "peso_compra": 2.0,
                    "valor_com_icms_compra": 20.0,
                    "percentual_icms_compra": 0.17,
                    "outras_despesas_item": 1.0,
                    "peso_venda": 2.0,
                    "valor_com_icms_venda": 35.0,
                    "percentual_icms_venda": 0.17,
                    "percentual_ipi": 0.05,
                    "delivery_time": "0"  # CAMPO PRAZO - imediato
                }
            ]
        }
        
        print("2. Dados do orçamento preparados:")
        for i, item in enumerate(budget_data["items"]):
            print(f"   Item {i+1}: {item['description']} - Prazo: {item['delivery_time']} dias")
        
        # 3. Criar orçamento usando endpoint simplificado
        print("\n3. Criando orçamento via endpoint simplificado...")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{BASE_URL_BUDGET}/api/v1/budgets/simplified",
                headers={**headers, "Content-Type": "application/json"},
                data=json.dumps(budget_data)
            ) as response:
                
                if response.status != 201:
                    error_text = await response.text()
                    print(f"❌ ERRO na criação: Status {response.status}")
                    print(f"   Resposta: {error_text}")
                    return False
                
                created_budget = await response.json()
                budget_id = created_budget["id"]
                order_number = created_budget["order_number"]
                
                print(f"✅ Orçamento criado com sucesso!")
                print(f"   ID: {budget_id}")
                print(f"   Número: {order_number}")
        
        # 4. Buscar orçamento criado para verificar se os valores de PRAZO foram salvos
        print(f"\n4. Verificando orçamento criado (ID: {budget_id})...")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL_BUDGET}/api/v1/budgets/{budget_id}",
                headers=headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    print(f"❌ ERRO na consulta: Status {response.status}")
                    print(f"   Resposta: {error_text}")
                    return False
                
                retrieved_budget = await response.json()
        
        # 5. Validar se os valores de PRAZO foram salvos corretamente
        print("\n5. Validando valores de PRAZO salvos:")
        items = retrieved_budget.get("items", [])
        expected_delivery_times = ["15", "30", "0"]
        
        success = True
        for i, item in enumerate(items):
            expected_time = expected_delivery_times[i]
            actual_time = item.get("delivery_time")
            
            print(f"   Item {i+1}: {item.get('description', 'N/A')}")
            print(f"      Prazo esperado: {expected_time} dias")
            print(f"      Prazo salvo: {actual_time}")
            
            if str(actual_time) == str(expected_time):
                print(f"      ✅ CORRETO")
            else:
                print(f"      ❌ INCORRETO - Esperado: {expected_time}, Obtido: {actual_time}")
                success = False
        
        # 6. Teste adicional: verificar diretamente no banco via endpoint debug
        print(f"\n6. Verificação adicional via endpoint debug...")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL_BUDGET}/api/v1/budgets/debug-delivery/{budget_id}",
                headers=headers
            ) as response:
                
                if response.status == 200:
                    debug_data = await response.json()
                    print("   Dados diretos do banco:")
                    for item in debug_data.get("items", []):
                        print(f"      ID {item['id']}: {item['description']}")
                        print(f"         delivery_time_raw: {item['delivery_time_raw']}")
                        print(f"         delivery_time_repr: {item['delivery_time_repr']}")
                else:
                    print("   ⚠️  Endpoint debug não disponível ou erro")
        
        # 7. Resultado final
        print(f"\n{'='*60}")
        if success:
            print("🎉 TESTE PASSOU: Campo PRAZO está sendo salvo corretamente!")
            print("✅ Correção implementada com sucesso")
        else:
            print("❌ TESTE FALHOU: Campo PRAZO não está sendo salvo corretamente")
            print("⚠️  Correção precisa ser revisada")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERRO durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Função principal"""
    print("Iniciando teste de validação do campo PRAZO...")
    print(f"URL User Service: {BASE_URL_USER}")
    print(f"URL Budget Service: {BASE_URL_BUDGET}")
    print(f"Usuário: {TEST_USER['username']}")
    
    success = await test_prazo_field_creation()
    
    if success:
        print("\n🎯 CONCLUSÃO: O problema do campo PRAZO foi resolvido!")
    else:
        print("\n⚠️  CONCLUSÃO: O problema do campo PRAZO ainda existe!")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    exit(0 if result else 1)

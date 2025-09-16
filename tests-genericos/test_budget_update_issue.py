#!/usr/bin/env python3
"""
Teste para verificar o problema de atualização de orçamento
Problema relatado: ao editar um orçamento e salvar, é retornado sucesso mas não reflete a atualização.
"""

import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

# Configurações
BASE_URL = "http://localhost:8002"
API_URL = f"{BASE_URL}/api/v1"

# Credenciais de teste
TEST_USER = {
    "username": "admin",
    "password": "admin123"
}

class BudgetUpdateTest:
    def __init__(self):
        self.session = None
        self.token = None
        self.budget_id = None

    async def create_session(self):
        """Criar sessão HTTP"""
        self.session = aiohttp.ClientSession()

    async def close_session(self):
        """Fechar sessão HTTP"""
        if self.session:
            await self.session.close()

    async def login(self):
        """Fazer login e obter token"""
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        
        async with self.session.post(f"{API_URL}/auth/login", json=login_data) as response:
            if response.status == 200:
                data = await response.json()
                self.token = data["access_token"]
                print("✅ Login realizado com sucesso")
                return True
            else:
                error_text = await response.text()
                print(f"❌ Erro no login: {response.status} - {error_text}")
                return False

    def get_headers(self):
        """Obter headers com autorização"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def create_test_budget(self):
        """Criar um orçamento para teste"""
        budget_data = {
            "order_number": f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "client_name": "Cliente Teste Atualização",
            "notes": "Orçamento criado para teste de atualização",
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat(),
            "items": [
                {
                    "description": "Produto Teste Original",
                    "peso_compra": 1.0,
                    "peso_venda": 1.0,
                    "valor_com_icms_compra": 100.0,
                    "percentual_icms_compra": 0.18,
                    "outras_despesas_item": 0.0,
                    "valor_com_icms_venda": 150.0,
                    "percentual_icms_venda": 0.17
                }
            ]
        }

        async with self.session.post(
            f"{API_URL}/budgets/simplified", 
            json=budget_data,
            headers=self.get_headers()
        ) as response:
            if response.status == 201:
                budget = await response.json()
                self.budget_id = budget["id"]
                print(f"✅ Orçamento criado com sucesso - ID: {self.budget_id}")
                print(f"   - Cliente: {budget['client_name']}")
                print(f"   - Notas: {budget.get('notes', 'N/A')}")
                print(f"   - Items: {len(budget['items'])} item(s)")
                if budget['items']:
                    print(f"   - Primeiro item: {budget['items'][0]['description']}")
                return budget
            else:
                error_text = await response.text()
                print(f"❌ Erro ao criar orçamento: {response.status} - {error_text}")
                return None

    async def get_budget(self, budget_id):
        """Buscar orçamento por ID"""
        async with self.session.get(
            f"{API_URL}/budgets/{budget_id}",
            headers=self.get_headers()
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                print(f"❌ Erro ao buscar orçamento: {response.status} - {error_text}")
                return None

    async def update_budget(self, budget_id):
        """Tentar atualizar o orçamento usando a mesma lógica do frontend"""
        print(f"\n🔄 Testando atualização do orçamento {budget_id}...")
        
        # Primeiro, buscar o orçamento atual
        current_budget = await self.get_budget(budget_id)
        if not current_budget:
            return False

        print("📖 Estado atual do orçamento:")
        print(f"   - Cliente: {current_budget['client_name']}")
        print(f"   - Notas: {current_budget.get('notes', 'N/A')}")
        
        # Criar dados de atualização simulando o frontend
        # (seguindo a mesma lógica do BudgetEditSimplified.tsx)
        update_data = {
            "order_number": current_budget["order_number"],
            "client_name": "Cliente Teste ATUALIZADO",
            "status": current_budget["status"],
            "expires_at": current_budget.get("expires_at"),
            "notes": "Notas ATUALIZADAS pelo teste",
            "markup_percentage": 0,  # Será calculado automaticamente
            "items": []
        }

        # Converter items para formato completo (como faz o frontend)
        for item in current_budget["items"]:
            converted_item = {
                "description": "Produto Teste ATUALIZADO",  # Mudança principal
                "quantity": 1,
                "weight": item.get("weight", 1.0),
                "sale_weight": item.get("sale_weight", item.get("weight", 1.0)),
                "purchase_value_with_icms": item.get("purchase_value_with_icms", 100.0),
                "purchase_icms_percentage": item.get("purchase_icms_percentage", 18.0),
                "purchase_other_expenses": item.get("purchase_other_expenses", 0.0),
                "purchase_value_without_taxes": 0,  # Será calculado
                "sale_value_with_icms": item.get("sale_value_with_icms", 150.0),
                "sale_icms_percentage": item.get("sale_icms_percentage", 17.0),
                "sale_value_without_taxes": 0,  # Será calculado
                "commission_percentage": 5,  # Valor padrão
                "dunamis_cost": 0,
            }
            update_data["items"].append(converted_item)

        print("🔄 Enviando dados de atualização:")
        print(f"   - Cliente: {update_data['client_name']}")
        print(f"   - Notas: {update_data['notes']}")
        if update_data["items"]:
            print(f"   - Primeiro item: {update_data['items'][0]['description']}")

        # Enviar atualização
        async with self.session.put(
            f"{API_URL}/budgets/{budget_id}",
            json=update_data,
            headers=self.get_headers()
        ) as response:
            if response.status == 200:
                updated_budget = await response.json()
                print("✅ Atualização retornou sucesso!")
                print(f"   - Cliente retornado: {updated_budget['client_name']}")
                print(f"   - Notas retornadas: {updated_budget.get('notes', 'N/A')}")
                if updated_budget['items']:
                    print(f"   - Primeiro item retornado: {updated_budget['items'][0]['description']}")
                return updated_budget
            else:
                error_text = await response.text()
                print(f"❌ Erro na atualização: {response.status} - {error_text}")
                return None

    async def verify_update(self, budget_id):
        """Verificar se a atualização foi realmente salva"""
        print(f"\n🔍 Verificando se a atualização foi salva...")
        
        # Buscar o orçamento novamente para verificar
        updated_budget = await self.get_budget(budget_id)
        if not updated_budget:
            return False

        print("📖 Estado após atualização:")
        print(f"   - Cliente: {updated_budget['client_name']}")
        print(f"   - Notas: {updated_budget.get('notes', 'N/A')}")
        if updated_budget['items']:
            print(f"   - Primeiro item: {updated_budget['items'][0]['description']}")

        # Verificar se as mudanças foram salvas
        changes_saved = (
            updated_budget['client_name'] == "Cliente Teste ATUALIZADO" and
            updated_budget.get('notes') == "Notas ATUALIZADAS pelo teste" and
            updated_budget['items'] and
            updated_budget['items'][0]['description'] == "Produto Teste ATUALIZADO"
        )

        if changes_saved:
            print("✅ SUCESSO: As atualizações foram salvas corretamente!")
            return True
        else:
            print("❌ PROBLEMA CONFIRMADO: As atualizações NÃO foram salvas!")
            print("   - Este é o bug relatado pelo usuário")
            return False

    async def run_test(self):
        """Executar o teste completo"""
        print("🧪 Iniciando teste de atualização de orçamento...")
        print("=" * 60)

        try:
            # Configurar
            await self.create_session()
            
            # Login
            if not await self.login():
                return False

            # Criar orçamento de teste
            budget = await self.create_test_budget()
            if not budget:
                return False

            # Aguardar um pouco
            await asyncio.sleep(1)

            # Tentar atualizar
            updated_budget = await self.update_budget(self.budget_id)
            if not updated_budget:
                return False

            # Aguardar um pouco
            await asyncio.sleep(1)

            # Verificar se foi salvo
            success = await self.verify_update(self.budget_id)
            
            print("=" * 60)
            if success:
                print("🎉 TESTE PASSOU: Sistema funcionando corretamente!")
            else:
                print("🚨 TESTE FALHOU: Bug confirmado - atualizações não estão sendo salvas!")
            
            return success

        except Exception as e:
            print(f"❌ Erro durante o teste: {str(e)}")
            return False
        finally:
            await self.close_session()

async def main():
    """Função principal"""
    test = BudgetUpdateTest()
    success = await test.run_test()
    
    if not success:
        print("\n🔧 DIAGNÓSTICO:")
        print("O problema parece estar na lógica de atualização.")
        print("Possíveis causas:")
        print("1. O endpoint PUT não está processando todos os campos")
        print("2. A conversão de dados no frontend está incorreta") 
        print("3. O schema BudgetUpdate não inclui os campos necessários")
        print("4. Os items não estão sendo atualizados, apenas os campos do orçamento")

if __name__ == "__main__":
    asyncio.run(main())

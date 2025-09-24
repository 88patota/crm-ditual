#!/usr/bin/env python3
"""
Script para testar o endpoint de dashboard diretamente
"""

import requests
import json

def test_dashboard_endpoint():
    """Testa o endpoint de dashboard"""
    try:
        url = "http://localhost:3000/api/v1/dashboard/stats"
        params = {"days": 30}
        
        print(f"Testando: {url}")
        print(f"Parâmetros: {params}")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print("❌ Erro!")
            print(f"Texto da resposta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    test_dashboard_endpoint()

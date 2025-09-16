#!/bin/bash
# Script simples para testar o endpoint

echo "=== Testando endpoint de dashboard ==="
echo "URL: http://localhost:3000/api/v1/dashboard/stats?days=30"
echo

# Fazer requisição
curl -X GET "http://localhost:3000/api/v1/dashboard/stats?days=30" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -w "\nStatus Code: %{http_code}\n" \
     -s

echo
echo "=== Teste concluído ==="

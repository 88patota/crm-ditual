#!/bin/bash
echo "🔍 Testando login com diferentes credenciais..."

echo "1. Testando admin/admin123:"
RESPONSE1=$(curl -s -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123")
echo "Resposta: $RESPONSE1"

echo "2. Testando admin/123456:"
RESPONSE2=$(curl -s -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456")
echo "Resposta: $RESPONSE2"

echo "3. Testando formato JSON:"
RESPONSE3=$(curl -s -X POST "http://localhost:8001/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}')
echo "Resposta: $RESPONSE3"
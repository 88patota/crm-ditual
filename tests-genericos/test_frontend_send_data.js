// Teste para simular como o frontend está enviando dados
const testData = {
    "order_number": "PED-0001",
    "client_name": "Cliente Teste",
    "status": "draft",
    "expires_at": "2025-08-19T03:00:00.000Z",
    "prazo_medio": 1,
    "outras_despesas_totais": 0,
    "items": [{
        "description": "item",
        "quantity": 5,
        "peso_compra": 5.500,  // Problema aqui - deveria manter 5.500
        "peso_venda": 5.5,
        "valor_com_icms_compra": 3.45,
        "percentual_icms_compra": 0.12,
        "outras_despesas_item": 0,
        "valor_com_icms_venda": 46,
        "percentual_icms_venda": 0.12
    }]
};

console.log("=== TESTE FRONTEND SEND DATA ===");
console.log("1. Dados originais:");
console.log("peso_compra:", testData.items[0].peso_compra);
console.log("tipo:", typeof testData.items[0].peso_compra);

console.log("\n2. Serialização JSON:");
const jsonString = JSON.stringify(testData);
console.log("JSON String:", jsonString);

console.log("\n3. Parse do JSON:");
const parsedData = JSON.parse(jsonString);
console.log("peso_compra após parse:", parsedData.items[0].peso_compra);
console.log("tipo após parse:", typeof parsedData.items[0].peso_compra);

console.log("\n4. Problema identificado:");
if (parsedData.items[0].peso_compra !== testData.items[0].peso_compra) {
    console.log("❌ VALOR PERDIDO NA SERIALIZAÇÃO!");
} else {
    console.log("✅ Valor preservado na serialização");
}

// Teste específico com diferentes valores
const testValues = [5.0, 5.5, 5.50, 5.500, 5.555];
console.log("\n5. Teste com diferentes valores:");
testValues.forEach(val => {
    const testObj = { peso: val };
    const jsonStr = JSON.stringify(testObj);
    const parsed = JSON.parse(jsonStr);
    console.log(`${val} -> ${parsed.peso} (preservado: ${val === parsed.peso})`);
});

// Simulação do que pode estar acontecendo no InputNumber
console.log("\n6. Simulação InputNumber onChange:");
function simulateInputNumberChange(value) {
    console.log(`Input: ${value} (tipo: ${typeof value})`);
    
    // Simular parse que pode acontecer no InputNumber
    const numericValue = typeof value === 'number' ? value : parseFloat(value) || 0;
    console.log(`Depois do processamento: ${numericValue} (tipo: ${typeof numericValue})`);
    
    return numericValue;
}

simulateInputNumberChange("5.500");
simulateInputNumberChange(5.500);
simulateInputNumberChange("5");

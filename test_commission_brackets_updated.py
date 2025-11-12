#!/usr/bin/env python3
"""
Teste das novas faixas de comissão atualizadas
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'budget_service'))

from app.services.commission_service import CommissionService

def test_new_commission_brackets():
    """Testa as novas faixas de comissão"""
    
    print("🧪 Testando as novas faixas de comissão:")
    print("=" * 50)
    
    # Casos de teste com as novas faixas
    test_cases = [
        # (rentabilidade_percentual, comissao_esperada_percentual, descricao)
        (10.0, 0.0, "10% - deve ser 0%"),
        (19.99, 0.0, "19.99% - deve ser 0%"),
        (20.0, 1.0, "20% - deve ser 1%"),
        (25.0, 1.0, "25% - deve ser 1%"),
        (29.99, 1.0, "29.99% - deve ser 1%"),
        (30.0, 1.5, "30% - deve ser 1.5%"),
        (35.0, 1.5, "35% - deve ser 1.5%"),
        (39.99, 1.5, "39.99% - deve ser 1.5%"),
        (40.0, 2.5, "40% - deve ser 2.5%"),
        (45.0, 2.5, "45% - deve ser 2.5%"),
        (49.99, 2.5, "49.99% - deve ser 2.5%"),
        (50.0, 3.0, "50% - deve ser 3%"),
        (55.0, 3.0, "55% - deve ser 3%"),
        (59.99, 3.0, "59.99% - deve ser 3%"),
        (60.0, 4.0, "60% - deve ser 4%"),
        (70.0, 4.0, "70% - deve ser 4%"),
        (79.99, 4.0, "79.99% - deve ser 4%"),
        (80.0, 5.0, "80% - deve ser 5%"),
        (100.0, 5.0, "100% - deve ser 5%"),
    ]
    
    all_passed = True
    
    for rentabilidade_perc, comissao_esperada_perc, descricao in test_cases:
        # Converter para decimal (formato usado internamente)
        rentabilidade_decimal = rentabilidade_perc / 100.0
        comissao_esperada_decimal = comissao_esperada_perc / 100.0
        
        # Calcular comissão
        comissao_calculada = CommissionService.calculate_commission_percentage(rentabilidade_decimal)
        
        # Verificar resultado
        if abs(comissao_calculada - comissao_esperada_decimal) < 0.0001:
            status = "✅ PASSOU"
        else:
            status = "❌ FALHOU"
            all_passed = False
        
        print(f"{status} | {descricao}")
        print(f"    Rentabilidade: {rentabilidade_perc}% | Comissão calculada: {comissao_calculada*100}% | Esperada: {comissao_esperada_perc}%")
        print()
    
    print("=" * 50)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM! As novas faixas estão funcionando corretamente.")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM! Verifique a implementação.")
    
    return all_passed

def test_commission_calculation_example():
    """Testa um exemplo prático de cálculo de comissão"""
    
    print("\n💰 Exemplo prático de cálculo:")
    print("=" * 50)
    
    # Exemplo: Item com 35% de rentabilidade e R$ 1000 de venda
    rentabilidade = 0.35  # 35%
    valor_venda = 1000.0  # R$ 1000
    
    comissao_percentual = CommissionService.calculate_commission_percentage(rentabilidade)
    valor_comissao = CommissionService.calculate_commission_value(valor_venda, rentabilidade)
    
    print(f"📊 Item com rentabilidade de {rentabilidade*100}%")
    print(f"💵 Valor de venda: R$ {valor_venda:.2f}")
    print(f"📈 Faixa aplicada: 30-39,99% → {comissao_percentual*100}% de comissão")
    print(f"💰 Valor da comissão: R$ {valor_comissao:.2f}")
    
    # Verificar se está correto (35% deve dar 1.5% de comissão)
    if comissao_percentual == 0.015:  # 1.5%
        print("✅ Cálculo correto!")
    else:
        print("❌ Erro no cálculo!")

if __name__ == "__main__":
    print("🔧 Teste das Novas Faixas de Comissão")
    print("Versão atualizada conforme solicitação do usuário")
    print()
    
    # Executar testes
    success = test_new_commission_brackets()
    test_commission_calculation_example()
    
    if success:
        print("\n🚀 Sistema pronto para uso com as novas faixas!")
    else:
        print("\n🔧 Necessário revisar a implementação.")
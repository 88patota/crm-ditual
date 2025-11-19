"""
Testes de regressão para validar a migração para o ProfitabilityService.

Estes testes garantem que:
1. As regras válidas de comissão (SEM ICMS) estão corretas
2. A rentabilidade para display (COM ICMS) é mantida
3. Os valores de comissão são calculados corretamente
"""

import sys
import os
import unittest
from decimal import Decimal

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.profitability_service import ProfitabilityService
from services.business_rules_calculator_refactored import BusinessRulesCalculatorRefactored


class TestRegressaoRentabilidade(unittest.TestCase):
    """Testes de regressão para garantir a qualidade da migração."""
    
    def setUp(self):
        """Configurar dados de teste."""
        # Dados de exemplo baseados em casos reais
        self.item_data = {
            'description': 'Item Teste',
            'peso_compra': 100.0,
            'peso_venda': 100.0,
            'valor_com_icms_compra': 10.0,  # R$ 10,00 com ICMS
            'valor_com_icms_venda': 15.0,   # R$ 15,00 com ICMS
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'percentual_ipi': 0.10,
            'outras_despesas_item': 0.0
        }
        
        # Valores sem ICMS (18% ICMS + 9.5% PIS/COFINS = 27.5% total)
        self.valor_compra_sem_icms = Decimal('10.0') / Decimal('1.275')  # ~R$ 7,84
        self.valor_venda_sem_icms = Decimal('15.0') / Decimal('1.275')   # ~R$ 11,76
        
        self.frete_total = 50.0
        self.peso_total = 1000.0
        self.outras_despesas = 0.0
    
    def test_rentabilidade_item_sem_icms_regra_valida(self):
        """Testa regra válida: rentabilidade por item SEM ICMS."""
        # Arrange
        valor_esperado = (self.valor_venda_sem_icms / self.valor_compra_sem_icms - 1)
        
        # Act
        resultado = ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_item_sem_icms=self.valor_venda_sem_icms,
            valor_compra_item_sem_icms=self.valor_compra_sem_icms
        )
        
        # Assert
        self.assertAlmostEqual(float(resultado), float(valor_esperado), places=4)
        print(f"✅ Rentabilidade item sem ICMS: {resultado:.4f} ({resultado*100:.2f}%)")
    
    def test_rentabilidade_item_com_frete_diluido(self):
        """Testa regra válida: frete diluído pelo peso."""
        # Arrange
        frete_por_kg = Decimal(str(self.frete_total)) / Decimal(str(self.peso_total))
        frete_diluido_item = frete_por_kg * Decimal('100.0')  # 100kg do item
        valor_compra_com_frete = self.valor_compra_sem_icms + frete_diluido_item
        valor_esperado = (self.valor_venda_sem_icms / valor_compra_com_frete - 1)
        
        # Act
        resultado = ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_item_sem_icms=self.valor_venda_sem_icms,
            valor_compra_item_sem_icms=self.valor_compra_sem_icms,
            freight_value=self.frete_total,
            purchase_weight=100.0,
            total_purchase_weight=self.peso_total
        )
        
        # Assert
        self.assertAlmostEqual(float(resultado), float(valor_esperado), places=4)
        print(f"✅ Rentabilidade com frete: {resultado:.4f} ({resultado*100:.2f}%)")
    
    def test_rentabilidade_orcamento_sem_icms_regra_valida(self):
        """Testa regra válida: rentabilidade do orçamento SEM ICMS."""
        # Arrange
        total_venda_sem_icms = self.valor_venda_sem_icms * Decimal('100.0')  # 100kg
        total_compra_sem_icms = self.valor_compra_sem_icms * Decimal('100.0')  # 100kg
        valor_esperado = (total_venda_sem_icms / total_compra_sem_icms - 1)
        
        # Act
        resultado = ProfitabilityService.calculate_budget_profitability(
            valor_total_venda_sem_icms=total_venda_sem_icms,
            valor_total_compra_sem_icms=total_compra_sem_icms
        )
        
        # Assert
        self.assertAlmostEqual(float(resultado), float(valor_esperado), places=4)
        print(f"✅ Rentabilidade orçamento sem ICMS: {resultado:.4f} ({resultado*100:.2f}%)")
    
    def test_rentabilidade_display_com_icms(self):
        """Testa rentabilidade para display (COM ICMS)."""
        # Arrange
        valor_venda_com_icms = Decimal('15.0')
        valor_compra_com_icms = Decimal('10.0')
        valor_esperado = (valor_venda_com_icms / valor_compra_com_icms - 1)
        
        # Act
        resultado = ProfitabilityService.calculate_display_profitability(
            valor_venda_item_com_icms=valor_venda_com_icms,
            valor_compra_item_com_icms=valor_compra_com_icms,
            usar_valores_com_icms=True
        )
        
        # Assert
        self.assertAlmostEqual(float(resultado), float(valor_esperado), places=4)
        print(f"✅ Rentabilidade display com ICMS: {resultado:.4f} ({resultado*100:.2f}%)")
    
    def test_comparacao_rentabilidade_display_vs_comissao(self):
        """Compara rentabilidade de display e de comissão (ambas SEM ICMS após virada)."""
        # Rentabilidade SEM ICMS (comissão)
        rentabilidade_sem_icms = ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_item_sem_icms=self.valor_venda_sem_icms,
            valor_compra_item_sem_icms=self.valor_compra_sem_icms
        )

        # Rentabilidade para display agora também SEM ICMS
        rentabilidade_display_sem_icms = ProfitabilityService.calculate_display_profitability(
            valor_venda_item_sem_icms=self.valor_venda_sem_icms,
            valor_compra_item_sem_icms=self.valor_compra_sem_icms,
            usar_valores_com_icms=False
        )

        print(f"📊 Comparação (SEM ICMS):")
        print(f"   Comissão: {rentabilidade_sem_icms:.4f} ({rentabilidade_sem_icms*100:.2f}%)")
        print(f"   Display:  {rentabilidade_display_sem_icms:.4f} ({rentabilidade_display_sem_icms*100:.2f}%)")

        # As rentabilidades devem ser equivalentes dentro de uma tolerância
        self.assertAlmostEqual(float(rentabilidade_sem_icms), float(rentabilidade_display_sem_icms), places=4)
    
    def test_business_rules_calculator_refactored_item(self):
        """Testa o BusinessRulesCalculatorRefactored com item completo."""
        # Arrange
        item_data = self.item_data.copy()
        item_data['peso_venda'] = 100.0
        item_data['peso_compra'] = 100.0
        
        # Act
        resultado = BusinessRulesCalculatorRefactored.calculate_complete_item_refactored(
            item_data=item_data,
            outras_despesas_totais=0.0,
            soma_pesos_pedido=100.0,
            freight_value_total=0.0
        )
        
        # Assert - Verificar que temos ambas as rentabilidades
        self.assertIn('rentabilidade_item', resultado)      # Display (com ICMS)
        self.assertIn('rentabilidade_comissao', resultado)  # Comissão (sem ICMS)
        self.assertIn('percentual_comissao', resultado)     # Baseado em rentabilidade_comissao
        
        # A rentabilidade de comissão deve ser equivalente à de display (ambas SEM ICMS)
        rentabilidade_display = resultado['rentabilidade_item']
        rentabilidade_comissao = resultado['rentabilidade_comissao']
        
        self.assertAlmostEqual(float(rentabilidade_display), float(rentabilidade_comissao), places=4)
        
        print(f"✅ BusinessRulesCalculatorRefactored:")
        print(f"   Rentabilidade display:  {rentabilidade_display:.4f} ({rentabilidade_display*100:.2f}%)")
        print(f"   Rentabilidade comissão: {rentabilidade_comissao:.4f} ({rentabilidade_comissao*100:.2f}%)")
        print(f"   Percentual comissão:    {resultado['percentual_comissao']:.2f}%")
    
    def test_caso_edge_valores_zerados(self):
        """Testa casos edge com valores zerados."""
        # Act & Assert
        resultado = ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_item_sem_icms=0,
            valor_compra_item_sem_icms=0
        )
        self.assertEqual(resultado, Decimal('0'))
        
        resultado = ProfitabilityService.calculate_item_profitability_without_taxes(
            valor_venda_item_sem_icms=100,
            valor_compra_item_sem_icms=0
        )
        self.assertEqual(resultado, Decimal('0'))
        
        print("✅ Casos edge com valores zerados tratados corretamente")
    
    def test_conversao_percentual(self):
        """Testa conversão de decimal para percentual."""
        # Arrange
        valor_decimal = Decimal('0.25')  # 25%
        
        # Act
        percentual = ProfitabilityService.convert_to_percentage(valor_decimal)
        
        # Assert
        self.assertEqual(percentual, Decimal('25.00'))
        print(f"✅ Conversão percentual: {valor_decimal} → {percentual}%")


class TestValidacaoMigracao(unittest.TestCase):
    """Testes para validar que a migração não quebra funcionalidade existente."""
    
    def test_estrutura_resposta_mantida(self):
        """Garante que a estrutura da resposta é mantida para compatibilidade."""
        # Arrange
        item_data = {
            'description': 'Item Teste',
            'peso_compra': 100.0,
            'peso_venda': 100.0,
            'valor_com_icms_compra': 10.0,
            'valor_com_icms_venda': 15.0,
            'percentual_icms_compra': 0.18,
            'percentual_icms_venda': 0.18,
            'percentual_ipi': 0.10,
            'outras_despesas_item': 0.0
        }
        
        # Act
        resultado = BusinessRulesCalculatorRefactored.calculate_complete_item_refactored(
            item_data=item_data,
            outras_despesas_totais=0.0,
            soma_pesos_pedido=100.0,
            freight_value_total=0.0
        )
        
        # Assert - Campos obrigatórios devem existir
        campos_obrigatorios = [
            'description', 'peso_compra', 'peso_venda',
            'valor_com_icms_compra', 'valor_com_icms_venda',
            'rentabilidade_item', 'valor_comissao', 'percentual_comissao',
            'total_compra_item', 'total_venda_item'
        ]
        
        for campo in campos_obrigatorios:
            self.assertIn(campo, resultado, f"Campo obrigatório ausente: {campo}")
        
        # Novo campo adicionado
        self.assertIn('rentabilidade_comissao', resultado)
        
        print("✅ Estrutura de resposta mantida com novo campo adicionado")


if __name__ == '__main__':
    print("🧪 Iniciando testes de regressão para migração de rentabilidade...\n")
    
    # Executar testes com mais detalhes
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ Todos os testes de regressão passaram!")
        print("✅ A migração para o ProfitabilityService está pronta para produção.")
    else:
        print("\n❌ Alguns testes falharam. Revisar antes da migração.")
        sys.exit(1)
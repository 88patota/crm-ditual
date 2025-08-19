#!/usr/bin/env python3
"""
Script de teste para verificar a funcionalidade de geração de PDF
"""

import sys
import os
from datetime import datetime

# Adicionar o diretório do budget service ao path
sys.path.insert(0, '/Users/erikpatekoski/dev/crm-ditual/services/budget_service')

try:
    from app.services.pdf_export_service import PDFExportService
    from app.models.budget import Budget, BudgetItem, BudgetStatus
    print("✅ Importações realizadas com sucesso!")
    
    # Criar dados de teste
    class MockBudget:
        def __init__(self):
            self.id = 1
            self.order_number = "PED-0001"
            self.client_name = "TIZIANI"
            self.markup_percentage = 30.77
            self.total_purchase_value = 483.70
            self.total_sale_value = 632.53
            self.total_commission = 12.75
            self.profitability_percentage = 30.77
            self.status = type('Status', (), {'value': 'draft'})()
            self.notes = "Proposta teste - gerada automaticamente pelo sistema."
            self.created_by = "Sistema"
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.expires_at = None
            self.items = [MockBudgetItem()]
    
    class MockBudgetItem:
        def __init__(self):
            self.id = 1
            self.description = "TB QDR. 20 X 20 X 1,25 ZINCADO"
            self.quantity = 100
            self.weight = 100
            self.purchase_value_with_icms = 6.50
            self.purchase_icms_percentage = 18.0
            self.purchase_other_expenses = 0.0
            self.purchase_value_without_taxes = 4.84
            self.sale_weight = 100
            self.sale_value_with_icms = 8.50
            self.sale_icms_percentage = 18.0
            self.sale_value_without_taxes = 6.33
            self.profitability = 30.77
            self.total_purchase = 483.70
            self.total_sale = 632.53
            self.unit_value = 8.50
            self.total_value = 850.00
            self.commission_percentage = 1.50
            self.commission_value = 12.75
    
    # Testar geração de PDF
    pdf_service = PDFExportService()
    mock_budget = MockBudget()
    
    print("🔄 Testando geração de PDF completo...")
    pdf_content = pdf_service.generate_proposal_pdf(mock_budget)
    print(f"✅ PDF completo gerado! Tamanho: {len(pdf_content)} bytes")
    
    print("🔄 Testando geração de PDF simplificado...")
    pdf_simple = pdf_service.generate_simplified_proposal_pdf(mock_budget)
    print(f"✅ PDF simplificado gerado! Tamanho: {len(pdf_simple)} bytes")
    
    # Salvar PDFs de teste
    with open('/tmp/teste_proposta_completa.pdf', 'wb') as f:
        f.write(pdf_content)
    print("📄 PDF completo salvo em: /tmp/teste_proposta_completa.pdf")
    
    with open('/tmp/teste_proposta_simplificada.pdf', 'wb') as f:
        f.write(pdf_simple)
    print("📄 PDF simplificado salvo em: /tmp/teste_proposta_simplificada.pdf")
    
    print("\n🎉 Teste de geração de PDF concluído com sucesso!")
    print("Você pode abrir os arquivos gerados para verificar o resultado.")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Verifique se todas as dependências estão instaladas.")
except Exception as e:
    print(f"❌ Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()

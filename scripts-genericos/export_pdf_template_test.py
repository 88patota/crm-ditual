#!/usr/bin/env python3
"""
Gera um PDF de proposta usando o template oficial sem depender do banco.
Cria objetos Budget e BudgetItem em memória e salva em /tmp/Proposta_TESTE.pdf
"""

from datetime import datetime
import os
import sys

# Garantir que o diretório raiz do projeto esteja no PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BSVC = os.path.join(ROOT, 'services', 'budget_service')
if ROOT not in sys.path:
    sys.path.append(ROOT)
if BSVC not in sys.path:
    sys.path.append(BSVC)

from services.budget_service.app.services.pdf_export_service import pdf_export_service
from services.budget_service.app.models.budget import Budget, BudgetItem


def main():
    # Criar orçamento em memória
    budget = Budget(
        order_number="PED-TESTE",
        client_name="CLIENTE TESTE",
        notes="",
        freight_type="FOB",
        payment_condition="À vista",
    )
    budget.created_by = "admin"
    budget.created_at = datetime.now()
    budget.expires_at = datetime.now()

    # Itens de exemplo
    item = BudgetItem(
        description="item",
        weight=1.0,
        delivery_time="0",  # IMEDIATO
        sale_value_with_icms=4.32,  # preço unitário
        sale_icms_percentage=0.18,
        ipi_percentage=0.0,
    )

    budget.items = [item]

    # Gerar PDF usando o método assíncrono do serviço
    import asyncio
    pdf_content = asyncio.get_event_loop().run_until_complete(
        pdf_export_service.generate_proposal_pdf(budget)
    )

    # Salvar
    out_path = "/tmp/Proposta_TESTE.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf_content)

    print(f"✅ PDF gerado e salvo em: {out_path} | tamanho: {len(pdf_content)} bytes")


if __name__ == "__main__":
    main()
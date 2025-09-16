#!/usr/bin/env python3
"""
Teste simples da geração de PDF sem dependências do banco de dados
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def test_pdf_generation():
    """Teste básico de geração de PDF"""
    
    print("🔄 Testando geração básica de PDF...")
    
    # Criar buffer para o PDF
    buffer = io.BytesIO()
    
    # Criar documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=30*mm,
        bottomMargin=30*mm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Adicionar estilo personalizado
    styles.add(ParagraphStyle(
        name='TitleMain',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f2937'),
        fontName='Helvetica-Bold'
    ))
    
    # Elementos do PDF
    story = []
    
    # Título
    title = Paragraph("PROPOSTA COMERCIAL - TESTE", styles['TitleMain'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Informações básicas
    info_data = [
        ['PEDIDO:', 'PED-0001', '', 'CLIENTE:', 'TIZIANI'],
        ['', '', '', 'MARKUP DO PEDIDO:', '30.77%'],
        ['', '', '', 'COMISSÃO (POR ITEM):', 'R$ 12.75']
    ]
    
    info_table = Table(info_data, colWidths=[25*mm, 40*mm, 10*mm, 35*mm, 50*mm])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (4, 0), (4, -1), colors.HexColor('#2563eb')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Tabela de itens de teste
    headers = ['Item', 'Descrição', 'Quantidade', 'Valor Unit.', 'Total']
    
    items_data = [
        headers,
        ['1', 'TB QDR. 20 X 20 X 1,25 ZINCADO', '100', 'R$ 8,50', 'R$ 850,00'],
        ['', 'TOTAL GERAL', '', '', 'R$ 850,00']
    ]
    
    items_table = Table(items_data, colWidths=[15*mm, 80*mm, 25*mm, 30*mm, 30*mm])
    items_table.setStyle(TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Dados
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        
        # Total
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3f4f6')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('TEXTCOLOR', (4, -1), (4, -1), colors.HexColor('#2563eb')),
        
        # Bordas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Resumo financeiro
    summary_title = Paragraph("RESUMO FINANCEIRO", styles['Heading2'])
    story.append(summary_title)
    
    summary_data = [
        ['Total Venda:', 'R$ 850,00'],
        ['Markup Aplicado:', '30,77%'],
        ['Rentabilidade:', '30,77%'],
    ]
    
    summary_table = Table(summary_data, colWidths=[40*mm, 30*mm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2563eb')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(summary_table)
    
    # Rodapé
    story.append(Spacer(1, 30))
    footer_text = f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    footer = Paragraph(footer_text, styles['Normal'])
    story.append(footer)
    
    # Construir PDF
    doc.build(story)
    
    buffer.seek(0)
    pdf_content = buffer.getvalue()
    
    print(f"✅ PDF gerado com sucesso! Tamanho: {len(pdf_content)} bytes")
    
    # Salvar arquivo de teste
    with open('/tmp/teste_proposta_funcional.pdf', 'wb') as f:
        f.write(pdf_content)
    
    print("📄 PDF salvo em: /tmp/teste_proposta_funcional.pdf")
    print("🎉 Teste de geração de PDF concluído com sucesso!")
    
    return pdf_content

if __name__ == "__main__":
    try:
        test_pdf_generation()
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

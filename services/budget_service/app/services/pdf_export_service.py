"""
Serviço para exportação de orçamentos em PDF
Baseado na estrutura da planilha de proposta fornecida
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import io
from typing import Dict, List, Any
from datetime import datetime
from app.models.budget import Budget, BudgetItem


class PDFExportService:
    """Serviço para exportar orçamentos como propostas em PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para o PDF"""
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='TitleMain',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f2937'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para cabeçalho da proposta
        self.styles.add(ParagraphStyle(
            name='ProposalHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para informações destacadas
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#2563eb'),
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para observações
        self.styles.add(ParagraphStyle(
            name='Notes',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=15,
            spaceAfter=15,
            leftIndent=20,
            rightIndent=20,
            textColor=colors.HexColor('#4b5563')
        ))
    
    def generate_proposal_pdf(self, budget: Budget) -> bytes:
        """Gera PDF da proposta baseado no orçamento"""
        
        buffer = io.BytesIO()
        
        # Criar documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=30*mm,
            bottomMargin=30*mm
        )
        
        # Elementos do PDF
        story = []
        
        # Cabeçalho da proposta
        self._add_header(story, budget)
        
        # Informações do pedido e cliente
        self._add_proposal_info(story, budget)
        
        # Tabela principal de itens (baseada na planilha)
        self._add_items_table(story, budget)
        
        # Resumo financeiro
        self._add_financial_summary(story, budget)
        
        # Observações
        if budget.notes:
            self._add_notes(story, budget.notes)
        
        # Rodapé com informações adicionais
        self._add_footer(story, budget)
        
        # Construir PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _add_header(self, story: List, budget: Budget):
        """Adiciona cabeçalho da proposta"""
        # Título principal
        title = Paragraph("PROPOSTA COMERCIAL", self.styles['TitleMain'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Linha separadora
        line_data = [[''] * 10]
        line_table = Table(line_data, colWidths=[20*mm] * 10)
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2563eb')),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 20))
    
    def _add_proposal_info(self, story: List, budget: Budget):
        """Adiciona informações básicas da proposta"""
        
        # Dados básicos em formato de tabela
        info_data = [
            ['PEDIDO:', budget.order_number, '', 'CLIENTE:', budget.client_name],
            ['', '', '', 'MARKUP DO PEDIDO:', f'{budget.markup_percentage:.2f}%'],
            ['', '', '', 'COMISSÃO (POR ITEM):', f'R$ {budget.total_commission:.2f}']
        ]
        
        info_table = Table(info_data, colWidths=[25*mm, 40*mm, 10*mm, 35*mm, 50*mm])
        info_table.setStyle(TableStyle([
            # Formatação geral
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            
            # Labels em negrito
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (3, 0), (3, -1), 'Helvetica-Bold'),
            
            # Valores destacados
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (4, 0), (4, -1), colors.HexColor('#2563eb')),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTNAME', (4, 0), (4, -1), 'Helvetica-Bold'),
            
            # Bordas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
    
    def _add_items_table(self, story: List, budget: Budget):
        """Adiciona tabela principal de itens baseada na estrutura da planilha"""
        
        # Cabeçalho da tabela (baseado na planilha)
        headers = [
            'DESCRIÇÃO',
            'COMPRA\nPeso',
            'COMPRA\nValor c/ICMS',
            'COMPRA\n%ICMS',
            'COMPRA\nOutras Despesas',
            'COMPRA\nValor s/Impostos',
            'VENDA\nPeso',
            'VENDA\nValor c/ICMS',
            'VENDA\n%ICMS',
            'VENDA\nValor s/Impostos',
            'Rentabilidade',
            'Total Compra',
            'Total Venda',
            'Valor Unitário',
            'Valor Total',
            '%Comissão',
            'Valor Comissão'
        ]
        
        # Preparar dados dos itens
        table_data = [headers]
        
        for item in budget.items:
            row = [
                item.description,
                f'{item.weight or 0:.2f}',
                f'R$ {item.purchase_value_with_icms:.2f}',
                f'{item.purchase_icms_percentage:.1f}%',
                f'R$ {item.purchase_other_expenses:.2f}',
                f'R$ {item.purchase_value_without_taxes:.2f}',
                f'{item.sale_weight or item.weight or 0:.2f}',
                f'R$ {item.sale_value_with_icms:.2f}',
                f'{item.sale_icms_percentage:.1f}%',
                f'R$ {item.sale_value_without_taxes:.2f}',
                f'{item.profitability:.2f}%',
                f'R$ {item.total_purchase:.2f}',
                f'R$ {item.total_sale:.2f}',
                f'R$ {item.unit_value:.2f}',
                f'R$ {item.total_value:.2f}',
                f'{item.commission_percentage:.2f}%',
                f'R$ {item.commission_value:.2f}'
            ]
            table_data.append(row)
        
        # Criar tabela com larguras apropriadas
        col_widths = [
            35*mm,  # Descrição
            12*mm,  # Peso compra
            18*mm,  # Valor compra
            12*mm,  # ICMS compra
            15*mm,  # Outras despesas
            18*mm,  # Valor s/impostos compra
            12*mm,  # Peso venda
            18*mm,  # Valor venda
            12*mm,  # ICMS venda
            18*mm,  # Valor s/impostos venda
            15*mm,  # Rentabilidade
            18*mm,  # Total compra
            18*mm,  # Total venda
            15*mm,  # Valor unitário
            18*mm,  # Valor total
            12*mm,  # % Comissão
            15*mm   # Valor comissão
        ]
        
        items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Estilo da tabela
        items_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Dados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Todos exceto descrição centralizados
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),     # Descrição alinhada à esquerda
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            
            # Bordas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Zebra striping para linhas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            
            # Destaque para colunas de valores
            ('TEXTCOLOR', (2, 1), (2, -1), colors.HexColor('#059669')),  # Valor compra
            ('TEXTCOLOR', (7, 1), (7, -1), colors.HexColor('#2563eb')),  # Valor venda
            ('TEXTCOLOR', (10, 1), (10, -1), colors.HexColor('#dc2626')), # Rentabilidade
            ('TEXTCOLOR', (16, 1), (16, -1), colors.HexColor('#7c3aed')), # Comissão
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 20))
    
    def _add_financial_summary(self, story: List, budget: Budget):
        """Adiciona resumo financeiro da proposta"""
        
        # Título da seção
        summary_title = Paragraph("RESUMO FINANCEIRO", self.styles['ProposalHeader'])
        story.append(summary_title)
        
        # Dados do resumo
        summary_data = [
            ['Total Compra:', f'R$ {budget.total_purchase_value:.2f}'],
            ['Total Venda:', f'R$ {budget.total_sale_value:.2f}'],
            ['Total Comissão:', f'R$ {budget.total_commission:.2f}'],
            ['Markup Aplicado:', f'{budget.markup_percentage:.2f}%'],
            ['Rentabilidade:', f'{budget.profitability_percentage:.2f}%'],
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
        story.append(Spacer(1, 20))
    
    def _add_notes(self, story: List, notes: str):
        """Adiciona observações à proposta"""
        notes_title = Paragraph("OBSERVAÇÕES", self.styles['ProposalHeader'])
        story.append(notes_title)
        
        notes_content = Paragraph(notes, self.styles['Notes'])
        story.append(notes_content)
        story.append(Spacer(1, 15))
    
    def _add_footer(self, story: List, budget: Budget):
        """Adiciona rodapé com informações adicionais"""
        
        footer_data = [
            [f'Data de geração: {datetime.now().strftime("%d/%m/%Y %H:%M")}'],
            [f'Criado por: {budget.created_by}'],
            [f'Status: {self._get_status_text(budget.status.value)}'],
        ]
        
        if budget.expires_at:
            footer_data.append([f'Válido até: {budget.expires_at.strftime("%d/%m/%Y")}'])
        
        footer_table = Table(footer_data, colWidths=[80*mm])
        footer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(Spacer(1, 20))
        story.append(footer_table)
    
    def _get_status_text(self, status: str) -> str:
        """Converte status para texto em português"""
        status_map = {
            'draft': 'Rascunho',
            'pending': 'Pendente',
            'approved': 'Aprovado',
            'rejected': 'Rejeitado',
            'expired': 'Expirado'
        }
        return status_map.get(status, status.title())
    
    def generate_simplified_proposal_pdf(self, budget: Budget) -> bytes:
        """Gera versão simplificada da proposta para apresentação ao cliente"""
        
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=30*mm,
            bottomMargin=30*mm
        )
        
        story = []
        
        # Cabeçalho simplificado
        title = Paragraph("PROPOSTA COMERCIAL", self.styles['TitleMain'])
        story.append(title)
        story.append(Spacer(1, 30))
        
        # Informações básicas
        info_data = [
            ['Pedido:', budget.order_number],
            ['Cliente:', budget.client_name],
            ['Data:', datetime.now().strftime("%d/%m/%Y")],
        ]
        
        if budget.expires_at:
            info_data.append(['Válido até:', budget.expires_at.strftime("%d/%m/%Y")])
        
        info_table = Table(info_data, colWidths=[30*mm, 60*mm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Tabela simplificada de itens
        simple_headers = ['Item', 'Descrição', 'Quantidade', 'Valor Unitário', 'Total']
        simple_data = [simple_headers]
        
        for i, item in enumerate(budget.items, 1):
            row = [
                str(i),
                item.description,
                f'{item.quantity:.0f}',
                f'R$ {item.unit_value:.2f}',
                f'R$ {item.total_value:.2f}'
            ]
            simple_data.append(row)
        
        # Linha de total
        simple_data.append([
            '', 'TOTAL GERAL', '', '', 
            f'R$ {budget.total_sale_value:.2f}'
        ])
        
        simple_table = Table(simple_data, colWidths=[15*mm, 80*mm, 25*mm, 30*mm, 30*mm])
        simple_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Dados
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Item
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Descrição
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'), # Quantidade, valores
            
            # Total
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3f4f6')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TEXTCOLOR', (4, -1), (4, -1), colors.HexColor('#2563eb')),
            
            # Bordas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(simple_table)
        
        # Observações se houver
        if budget.notes:
            story.append(Spacer(1, 30))
            self._add_notes(story, budget.notes)
        
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()


# Instância singleton do serviço
pdf_export_service = PDFExportService()

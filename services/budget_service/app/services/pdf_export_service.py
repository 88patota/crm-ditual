"""
Serviço para exportação de orçamentos em PDF
Template baseado na proposta oficial da Ditual São Paulo Tubos e Aços
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import io
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.models.budget import Budget, BudgetItem


class DitualPDFTemplate:
    """Template oficial da Ditual para propostas comerciais"""
    
    # Cores oficiais da Ditual (baseadas na proposta)
    DITUAL_RED = colors.HexColor('#8B1538')  # Vermelho escuro do cabeçalho
    DITUAL_GRAY = colors.HexColor('#4A4A4A')  # Cinza do texto
    DITUAL_LIGHT_GRAY = colors.HexColor('#F5F5F5')  # Cinza claro das linhas
    HEADER_BG = colors.HexColor('#8B1538')  # Fundo vermelho do cabeçalho
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.logo_path = self._get_logo_path()
    
    def _get_logo_path(self) -> Optional[str]:
        """
        Busca o logo da empresa em diferentes locais possíveis
        Para adicionar o logo, coloque o arquivo em uma dessas localizações:
        - /app/static/logo.png (dentro do container)
        - ./app/static/logo.png (relativo)
        - static/logo.png (relativo)
        """
        # Caminhos possíveis para o logo
        possible_paths = [
            "/app/static/logo.png",           # Caminho absoluto no container
            "/app/static/ditual_logo.png",    # Nome alternativo
            "app/static/logo.png",            # Relativo ao diretório de trabalho
            "app/static/ditual_logo.png",     # Nome alternativo relativo
            "static/logo.png",                # Relativo simples
            "static/ditual_logo.png",         # Nome alternativo simples
            "./app/static/logo.png",          # Explicitamente relativo
            os.path.join(os.path.dirname(__file__), "..", "static", "logo.png"),  # Relativo ao arquivo atual
            os.path.join(os.path.dirname(__file__), "..", "static", "ditual_logo.png")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def _setup_custom_styles(self):
        """Configura estilos customizados baseados no template da Ditual"""
        
        # Estilo para o cabeçalho principal
        self.styles.add(ParagraphStyle(
            name='DitualHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=0
        ))
        
        # Estilo para informações da empresa
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=0
        ))
        
        # Estilo para número da proposta
        self.styles.add(ParagraphStyle(
            name='ProposalNumber',
            parent=self.styles['Heading1'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=colors.white,
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0
        ))
        
        # Estilo para dados do cliente
        self.styles.add(ParagraphStyle(
            name='ClientLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_GRAY,
            alignment=TA_LEFT,
            spaceAfter=2,
            spaceBefore=2
        ))
        
        # Estilo para valores dos dados do cliente
        self.styles.add(ParagraphStyle(
            name='ClientValue',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=self.DITUAL_GRAY,
            alignment=TA_LEFT,
            spaceAfter=2,
            spaceBefore=2
        ))
        
        # Estilo para texto de introdução
        self.styles.add(ParagraphStyle(
            name='IntroText',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=self.DITUAL_GRAY,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            spaceBefore=10
        ))

    def generate_proposal_pdf(self, budget: Budget) -> bytes:
        """Gera PDF da proposta com template oficial da Ditual"""
        
        buffer = io.BytesIO()
        
        # Criar documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )
        
        # Elementos do PDF
        story = []
        
        # Cabeçalho oficial da Ditual
        self._add_ditual_header(story, budget)
        
        # Informações do cliente e proposta
        self._add_client_info(story, budget)
        
        # Texto de introdução
        self._add_intro_text(story)
        
        # Tabela principal de itens (exatamente como na proposta)
        self._add_items_table(story, budget)
        
        # Totais e condições
        self._add_totals_and_conditions(story, budget)
        
        # Observações se houver
        if budget.notes:
            self._add_observations(story, budget.notes)
        
        # Condições comerciais
        self._add_commercial_conditions(story, budget)
        
        # Rodapé com observações legais
        self._add_legal_footer(story)
        
        # Construir PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _add_ditual_header(self, story: List, budget: Budget):
        """Adiciona cabeçalho oficial da Ditual (fundo vermelho)"""
        
        # Dados da empresa (baseados na proposta)
        company_data = [
            [
                # Logo + Nome da empresa
                self._get_logo_cell(),
                # Informações da empresa
                Paragraph("""
                    Ditual São Paulo Tubos e Aços Ltda<br/>
                    Rua Joaquim Lobo, 81 - Pq São Miguel<br/>
                    Guarulhos/SP - CEP: 07260-080<br/>
                    CNPJ: 25.033.094/0001-26<br/>
                    I.E: 796.472.624.118
                """, self.styles['CompanyInfo']),
                # Número da proposta
                Paragraph(f"PROPOSTA:<br/><font size='16'>{budget.order_number}</font>", 
                         self.styles['ProposalNumber'])
            ]
        ]
        
        header_table = Table(company_data, colWidths=[60*mm, 80*mm, 50*mm])
        header_table.setStyle(TableStyle([
            # Fundo vermelho para toda a linha
            ('BACKGROUND', (0, 0), (-1, 0), self.HEADER_BG),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, 0), 8),
            ('RIGHTPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            # Bordas
            ('BOX', (0, 0), (-1, 0), 1, colors.black),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 5))
    
    def _get_logo_cell(self):
        """Retorna célula com logo da empresa ou espaço reservado"""
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                # Ajustar tamanho do logo proporcionalmente
                img = Image(self.logo_path, width=50*mm, height=25*mm)
                return img
            except Exception as e:
                print(f"Erro ao carregar logo: {e}")
                return Paragraph("<b>LOGO<br/>DITUAL</b>", self.styles['CompanyInfo'])
        else:
            # Placeholder para o logo
            return Paragraph("<b>LOGO<br/>DITUAL</b>", self.styles['CompanyInfo'])
    
    def _format_delivery_time(self, delivery_time: str) -> str:
        """Formata o prazo de entrega para exibição no PDF"""
        if not delivery_time:
            return "IMEDIATO"
        
        try:
            days = int(delivery_time)
            if days <= 0:
                return "IMEDIATO"
            elif days == 1:
                return "1 dia"
            else:
                return f"{days} dias"
        except (ValueError, TypeError):
            return delivery_time or "IMEDIATO"
    
    def _add_client_info(self, story: List, budget: Budget):
        """Adiciona informações do cliente e proposta"""
        
        # Formatar data
        created_date = budget.created_at.strftime('%d/%m/%Y') if budget.created_at else datetime.now().strftime('%d/%m/%Y')
        expires_date = budget.expires_at.strftime('%d/%m/%Y') if budget.expires_at else "7 dias corridos"
        
        # Dados do cliente e proposta
        client_data = [
            [
                Paragraph("Cliente:", self.styles['ClientLabel']),
                Paragraph(budget.client_name.upper(), self.styles['ClientValue']),
                "",
                Paragraph("Consultor:", self.styles['ClientLabel']),
                Paragraph(budget.created_by or "Sistema", self.styles['ClientValue'])
            ],
            [
                Paragraph("Contato:", self.styles['ClientLabel']),
                Paragraph("", self.styles['ClientValue']),  # Campo vazio para preenchimento manual
                "",
                Paragraph("Fone:", self.styles['ClientLabel']),
                Paragraph("", self.styles['ClientValue'])  # Campo vazio
            ],
            [
                Paragraph("Data:", self.styles['ClientLabel']),
                Paragraph(created_date, self.styles['ClientValue']),
                "",
                Paragraph("E-mail:", self.styles['ClientLabel']),
                Paragraph("", self.styles['ClientValue'])  # Campo vazio
            ],
            [
                Paragraph("Validade:", self.styles['ClientLabel']),
                Paragraph(expires_date, self.styles['ClientValue']),
                "",
                "",
                ""
            ]
        ]
        
        client_table = Table(client_data, colWidths=[20*mm, 50*mm, 10*mm, 25*mm, 85*mm])
        client_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            # Linha inferior
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ]))
        
        story.append(client_table)
        story.append(Spacer(1, 5))
    
    def _add_intro_text(self, story: List):
        """Adiciona texto de introdução da proposta"""
        intro_text = Paragraph(
            "Em atenção à sua solicitação, apresentamos abaixo condições comerciais para fornecimento dos itens consultados:",
            self.styles['IntroText']
        )
        story.append(intro_text)
        story.append(Spacer(1, 3))
    
    def _add_items_table(self, story: List, budget: Budget):
        """Adiciona tabela principal de itens (exatamente como na proposta)"""
        
        # Cabeçalho da tabela
        header_data = [
            [
                Paragraph("<b>Item</b>", self.styles['Normal']),
                Paragraph("<b>Dimensão mm</b>", self.styles['Normal']),
                Paragraph("<b>Unl</b>", self.styles['Normal']),
                Paragraph("<b>Qtd</b>", self.styles['Normal']),
                Paragraph("<b>Preço (R$)</b>", self.styles['Normal']),
                Paragraph("<b>ICMS</b>", self.styles['Normal']),
                Paragraph("<b>IPI a incluir</b>", self.styles['Normal']),
                Paragraph("<b>Valor total</b>", self.styles['Normal']),
                Paragraph("<b>Prazo de Entrega</b>", self.styles['Normal'])
            ]
        ]
        
        # Dados dos itens
        items_data = []
        for i, item in enumerate(budget.items, 1):
            items_data.append([
                str(i),
                Paragraph(item.description, self.styles['Normal']),
                "KG",
                f"{item.weight:,.0f}",
                f"R$ {item.sale_value_with_icms / item.weight:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                f"{item.sale_icms_percentage * 100:,.2f}%".replace('.', ','),
                f"{(item.ipi_percentage or 0) * 100:,.2f}%".replace('.', ','),
                f"R$ {item.total_sale:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                self._format_delivery_time(item.delivery_time)  # Formatar prazo de entrega
            ])
        
        # Adicionar linhas vazias para completar o template (reduzido para caber em uma página)
        for _ in range(max(0, 8 - len(budget.items))):
            items_data.append(["", "", "", "", "", "", "", "", ""])
        
        # Combinar cabeçalho e dados
        table_data = header_data + items_data
        
        # Larguras das colunas (ajustadas para A4)
        col_widths = [8*mm, 35*mm, 10*mm, 15*mm, 20*mm, 12*mm, 18*mm, 25*mm, 22*mm]
        
        items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        items_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), self.DITUAL_LIGHT_GRAY),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordas
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            
            # Alinhamento específico para colunas
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Descrição à esquerda
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),  # Números à direita
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 5))
    
    def _add_totals_and_conditions(self, story: List, budget: Budget):
        """Adiciona totais e peso (como na proposta)"""
        
        # Calcular totais
        total_weight = sum(item.weight for item in budget.items)
        total_without_ipi = budget.total_sale_value or 0
        total_with_ipi = budget.total_final_value or total_without_ipi
        
        # Tabela de totais
        totals_data = [
            [
                f"Peso Total: {total_weight:,.0f} kg".replace(',', '.'),
                "",
                f"Valor total S/IPI: R$ {total_without_ipi:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
                f"Valor total C/IPI: R$ {total_with_ipi:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            ]
        ]
        
        totals_table = Table(totals_data, colWidths=[50*mm, 50*mm, 45*mm, 45*mm])
        totals_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 8))
    
    def _add_observations(self, story: List, notes: str):
        """Adiciona seção de observações"""
        
        # Título
        obs_title = Paragraph("<b>Observações:</b>", self.styles['ClientLabel'])
        story.append(obs_title)
        story.append(Spacer(1, 5))
        
        # Caixa de observações
        obs_data = [[Paragraph(notes, self.styles['Normal'])]]
        obs_table = Table(obs_data, colWidths=[180*mm])
        obs_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(obs_table)
        story.append(Spacer(1, 8))
    
    def _add_commercial_conditions(self, story: List, budget: Budget):
        """Adiciona condições comerciais (como na proposta)"""
        
        # Título
        conditions_title = Paragraph("<b>Demais condições:</b>", self.styles['ClientLabel'])
        story.append(conditions_title)
        story.append(Spacer(1, 5))
        
        # Condições padrão
        conditions_data = [
            ["ICMS", "18,00%", "incluso"],
            ["PIS/COFINS", "9,25%", "incluso"],
            ["Condição de pagamento", "", "a combinar"],
            ["Frete", "", budget.freight_type or "FOB"],
            ["Embalagem", "", "fardo"]
        ]
        
        conditions_table = Table(conditions_data, colWidths=[40*mm, 30*mm, 110*mm])
        conditions_table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(conditions_table)
        story.append(Spacer(1, 10))
    
    def _add_legal_footer(self, story: List):
        """Adiciona rodapé com observações legais (como na proposta)"""
        
        legal_text = [
            "• Material sujeito a venda prévia / Os pesos informados são teóricos.",
            "• Após expiração da data de validade desta oferta, os preços estarão sujeitos a reajustes (para mais ou para menos) em função da variação dos preços dos aços planos praticados pelas usinas."
        ]
        
        for text in legal_text:
            legal_paragraph = Paragraph(text, self.styles['IntroText'])
            story.append(legal_paragraph)
            story.append(Spacer(1, 3))


class PDFExportService:
    """Serviço principal para exportação de PDF"""
    
    def __init__(self):
        self.template = DitualPDFTemplate()
    
    def generate_proposal_pdf(self, budget: Budget) -> bytes:
        """Gera PDF da proposta usando template oficial da Ditual"""
        return self.template.generate_proposal_pdf(budget)
    
    def generate_simplified_proposal_pdf(self, budget: Budget) -> bytes:
        """
        Mantido por compatibilidade, mas agora usa o mesmo template oficial
        """
        return self.template.generate_proposal_pdf(budget)


# Instância singleton do serviço
pdf_export_service = PDFExportService()
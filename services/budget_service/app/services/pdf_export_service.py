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
    """Template moderno da Ditual para propostas comerciais"""
    
    # Paleta de cores moderna e elegante
    DITUAL_RED = colors.HexColor('#8B1538')  # Vermelho principal da marca
    DITUAL_DARK_GRAY = colors.HexColor('#2C3E50')  # Cinza escuro para títulos
    DITUAL_GRAY = colors.HexColor('#5D6D7E')  # Cinza médio para texto
    DITUAL_LIGHT_GRAY = colors.HexColor('#ECF0F1')  # Cinza claro para fundos
    DITUAL_ACCENT = colors.HexColor('#E8F4FD')  # Azul claro para destaques
    HEADER_BG = colors.white  # Fundo branco moderno para o cabeçalho
    BORDER_COLOR = colors.HexColor('#BDC3C7')  # Cor suave para bordas
    
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
        """Configura estilos modernos e elegantes para o template"""
        
        # Estilo para o nome da empresa (destaque principal)
        self.styles.add(ParagraphStyle(
            name='CompanyName',
            parent=self.styles['Heading1'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_RED,
            alignment=TA_LEFT,
            spaceAfter=4,
            spaceBefore=0,
            leading=20
        ))
        
        # Estilo para informações da empresa (moderno e limpo)
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            textColor=self.DITUAL_GRAY,
            alignment=TA_LEFT,
            spaceAfter=1,
            spaceBefore=1,
            leading=11
        ))
        
        # Estilo para número da proposta (elegante)
        self.styles.add(ParagraphStyle(
            name='ProposalNumber',
            parent=self.styles['Heading1'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_RED,
            alignment=TA_CENTER,
            spaceAfter=0,
            spaceBefore=0,
            leading=18
        ))
        
        # Estilo para labels dos dados do cliente
        self.styles.add(ParagraphStyle(
            name='ClientLabel',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_DARK_GRAY,
            alignment=TA_LEFT,
            spaceAfter=3,
            spaceBefore=3,
            leading=12
        ))
        
        # Estilo para valores dos dados do cliente
        self.styles.add(ParagraphStyle(
            name='ClientValue',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.DITUAL_GRAY,
            alignment=TA_LEFT,
            spaceAfter=3,
            spaceBefore=3,
            leading=12
        ))
        
        # Estilo para texto de introdução
        self.styles.add(ParagraphStyle(
            name='IntroText',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            textColor=self.DITUAL_GRAY,
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            spaceBefore=12,
            leading=14
        ))
        
        # Estilo para cabeçalhos de seção
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_DARK_GRAY,
            alignment=TA_LEFT,
            spaceAfter=8,
            spaceBefore=15,
            leading=14
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
        """Adiciona cabeçalho moderno e elegante da Ditual"""
        
        # Dados da empresa atualizados
        company_data = [
            [
                # Logo + Nome da empresa
                self._get_logo_cell(),
                # Informações da empresa
                Paragraph("""
                    <b>DITUAL COMERCIO DE PRODUTOS ALIMENTICIOS LTDA</b><br/>
                    CNPJ: 33.200.056/0001-04<br/>
                    Rua Antônio Augusto Borges de Medeiros, 3339 - Sala 02<br/>
                    Exposição - Caxias do Sul/RS - CEP: 95084-460<br/>
                    Telefone: (54) 3025-3777 | E-mail: vendas@ditual.com.br
                """, self.styles['CompanyInfo']),
                # Número da proposta
                Paragraph(f"<b>PROPOSTA</b><br/>Nº {budget.order_number}", 
                         self.styles['ProposalNumber'])
            ]
        ]
        
        header_table = Table(company_data, colWidths=[70*mm, 90*mm, 50*mm])
        header_table.setStyle(TableStyle([
            # Fundo branco moderno
            ('BACKGROUND', (0, 0), (-1, 0), self.HEADER_BG),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, 0), 15),
            ('RIGHTPADDING', (0, 0), (-1, 0), 15),
            ('TOPPADDING', (0, 0), (-1, 0), 15),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            # Borda sutil na parte inferior
            ('LINEBELOW', (0, 0), (-1, 0), 2, self.BORDER_COLOR),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 25))
    
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
    
    def _format_currency(self, value: float) -> str:
        """Formata valores monetários com precisão e padrão brasileiro"""
        if value is None or value == 0:
            return "R$ 0,00"
        
        # Garantir precisão numérica e formatação brasileira
        formatted = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return formatted
    
    def _calculate_icms_value(self, item_value: float, icms_percentage: float, weight: float = 1.0) -> float:
        """Calcula o valor monetário do ICMS baseado no percentual e valor do item"""
        if not icms_percentage or not item_value:
            return 0.0
        
        # Calcular valor total do item
        total_item_value = item_value * weight
        # Calcular valor do ICMS
        icms_value = total_item_value * icms_percentage
        return icms_value
    
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
        
        # Cabeçalho da tabela com títulos otimizados para evitar quebras
        header_data = [
            [
                Paragraph("<b>Item</b>", self.styles['Normal']),
                Paragraph("<b>Descrição</b>", self.styles['Normal']),
                Paragraph("<b>Und</b>", self.styles['Normal']),
                Paragraph("<b>Qtd</b>", self.styles['Normal']),
                Paragraph("<b>Preço Unit.</b>", self.styles['Normal']),
                Paragraph("<b>ICMS</b>", self.styles['Normal']),
                Paragraph("<b>IPI (%)</b>", self.styles['Normal']),
                Paragraph("<b>Total</b>", self.styles['Normal']),
                Paragraph("<b>Prazo</b>", self.styles['Normal'])
            ]
        ]
        
        # Dados dos itens
        items_data = []
        for i, item in enumerate(budget.items, 1):
            # Calcular o preço unitário correto: valor total / peso (quantidade)
            # Se o peso for 0, usar o unit_value como fallback
            if item.weight and item.weight > 0:
                unit_price = (item.total_sale or 0) / item.weight
            else:
                unit_price = item.unit_value or 0
            
            # Calcular valor monetário do ICMS
            icms_value = self._calculate_icms_value(
                item.sale_value_with_icms, 
                item.sale_icms_percentage, 
                1.0  # Para valor unitário
            )
            
            items_data.append([
                str(i),
                Paragraph(item.description, self.styles['Normal']),
                "KG",
                f"{item.weight:,.0f}".replace(',', '.'),
                self._format_currency(unit_price),  # Valor unitário por unidade
                self._format_currency(icms_value) if icms_value > 0 else "R$ 0,00",  # ICMS em valor monetário
                f"{(item.ipi_percentage or 0) * 100:,.2f}%".replace('.', ','),
                self._format_currency(item.total_sale or 0),  # Formatação monetária melhorada
                self._format_delivery_time(item.delivery_time)
            ])
        
        # Combinar cabeçalho e dados (tabela dinâmica sem linhas vazias)
        table_data = header_data + items_data
        
        # Larguras das colunas otimizadas (Descrição com mais espaço para evitar quebras)
        col_widths = [10*mm, 45*mm, 8*mm, 12*mm, 18*mm, 12*mm, 15*mm, 22*mm, 18*mm]
        
        items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        items_table.setStyle(TableStyle([
            # Cabeçalho moderno e elegante
            ('BACKGROUND', (0, 0), (-1, 0), self.DITUAL_ACCENT),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.DITUAL_DARK_GRAY),
            
            # Corpo da tabela
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TEXTCOLOR', (0, 1), (-1, -1), self.DITUAL_GRAY),
            
            # Alinhamentos
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Descrição à esquerda
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),  # Números à direita
            
            # Bordas suaves e modernas
            ('LINEBELOW', (0, 0), (-1, 0), 2, self.DITUAL_RED),  # Linha vermelha sob cabeçalho
            ('GRID', (0, 1), (-1, -1), 0.5, self.BORDER_COLOR),  # Grade suave
            ('BOX', (0, 0), (-1, -1), 1, self.BORDER_COLOR),  # Borda externa suave
            
            # Padding generoso para melhor legibilidade
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            # Linhas alternadas para melhor leitura
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.DITUAL_LIGHT_GRAY]),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 5))
    
    def _add_totals_and_conditions(self, story: List, budget: Budget):
        """Adiciona totais e peso (como na proposta)"""
        
        # Calcular totais
        total_weight = sum(item.weight for item in budget.items)
        total_without_ipi = budget.total_sale_value or 0
        total_with_ipi = budget.total_final_value or total_without_ipi
        
        # Tabela de totais moderna e elegante
        totals_data = [
            [
                f"Peso Total: {total_weight:,.0f} kg".replace(',', '.'),
                "",
                f"Valor total S/IPI: {self._format_currency(total_without_ipi)}",
                f"Valor total C/IPI: {self._format_currency(total_with_ipi)}"
            ]
        ]
        
        totals_table = Table(totals_data, colWidths=[50*mm, 50*mm, 45*mm, 45*mm])
        totals_table.setStyle(TableStyle([
            # Estilo moderno para totais
            ('BACKGROUND', (0, 0), (-1, -1), self.DITUAL_LIGHT_GRAY),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.DITUAL_DARK_GRAY),
            ('ALIGN', (0, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Bordas elegantes
            ('BOX', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.DITUAL_RED),
            
            # Padding generoso
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 8))
    
    def _add_observations(self, story: List, notes: str):
        """Adiciona seção de observações com design moderno"""
        
        # Título elegante
        obs_title = Paragraph("Observações", self.styles['SectionHeader'])
        story.append(obs_title)
        
        # Caixa de observações moderna
        obs_data = [[Paragraph(notes, self.styles['IntroText'])]]
        obs_table = Table(obs_data, colWidths=[180*mm])
        obs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('BOX', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.DITUAL_ACCENT),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(obs_table)
        story.append(Spacer(1, 12))
    
    def _add_commercial_conditions(self, story: List, budget: Budget):
        """Adiciona condições comerciais com frete e pagamento destacados"""
        
        # Seção de Frete com design moderno
        freight_title = Paragraph("Condições de Frete", self.styles['SectionHeader'])
        story.append(freight_title)
        
        freight_type = budget.freight_type or "FOB"
        freight_description = "Por conta do destinatário" if freight_type == "FOB" else "Por conta do remetente"
        
        freight_data = [[
            Paragraph(f"<b>Tipo:</b> {freight_type} - {freight_description}", self.styles['ClientValue'])
        ]]
        
        freight_table = Table(freight_data, colWidths=[180*mm])
        freight_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.DITUAL_LIGHT_GRAY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.DITUAL_RED),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(freight_table)
        story.append(Spacer(1, 12))
        
        # Seção de Condições de Pagamento elegante
        payment_title = Paragraph("Condições de Pagamento", self.styles['SectionHeader'])
        story.append(payment_title)
        
        payment_condition = budget.payment_condition or "À vista"
        
        payment_data = [[
            Paragraph(f"<b>Condição:</b> {payment_condition}", self.styles['ClientValue'])
        ]]
        
        payment_table = Table(payment_data, colWidths=[180*mm])
        payment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.DITUAL_LIGHT_GRAY),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.DITUAL_RED),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(payment_table)
        story.append(Spacer(1, 15))
    
    def _add_legal_footer(self, story: List):
        """Adiciona rodapé elegante com observações legais"""
        
        # Título da seção
        footer_title = Paragraph("Observações Legais", self.styles['SectionHeader'])
        story.append(footer_title)
        
        legal_text = [
            "• Material sujeito a venda prévia / Os pesos informados são teóricos.",
            "• Após expiração da data de validade desta oferta, os preços estarão sujeitos a reajustes (para mais ou para menos) em função da variação dos preços dos aços planos praticados pelas usinas."
        ]
        
        # Criar uma caixa elegante para as observações legais
        legal_content = "<br/>".join(legal_text)
        legal_data = [[Paragraph(legal_content, self.styles['IntroText'])]]
        
        legal_table = Table(legal_data, colWidths=[180*mm])
        legal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.DITUAL_ACCENT),
            ('BOX', (0, 0), (-1, -1), 1, self.BORDER_COLOR),
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.DITUAL_GRAY),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(legal_table)


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
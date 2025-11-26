"""
Serviço para exportação de orçamentos em PDF
Template baseado na proposta oficial da Ditual São Paulo Tubos e Aços
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import io
import os
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from datetime import datetime
# Evitar import de modelos em tempo de execução para permitir uso do serviço
# em scripts independentes. Mantemos apenas para type checking.
if TYPE_CHECKING:  # pragma: no cover
    from app.models.budget import Budget, BudgetItem
from app.services.user_client import user_client, UserInfo
import logging

logger = logging.getLogger(__name__)


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
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_RED,
            alignment=TA_LEFT,
            spaceAfter=4,
            spaceBefore=0,
            leading=18
        ))
        
        # Estilo para informações da empresa (moderno e limpo)
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            textColor=self.DITUAL_GRAY,
            alignment=TA_LEFT,
            spaceAfter=1,
            spaceBefore=1,
            leading=10
        ))
        
        # Estilo para número da proposta (elegante)
        self.styles.add(ParagraphStyle(
            name='ProposalNumber',
            parent=self.styles['Heading1'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=self.DITUAL_RED,
            alignment=TA_RIGHT,
            spaceAfter=0,
            spaceBefore=0,
            leading=13
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

    async def generate_proposal_pdf(self, budget: Any, auth_token: Optional[str] = None) -> bytes:
        """Gera PDF da proposta com template oficial da Ditual"""
        
        # Obter informações completas do usuário
        user_info = None
        if auth_token and budget.created_by:
            try:
                user_info = await user_client.get_user_by_username(budget.created_by, auth_token)
            except Exception as e:
                logger.warning(f"Failed to get user info for {budget.created_by}: {e}")
        
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
        
        # Informações do cliente e proposta (com dados do usuário)
        self._add_client_info(story, budget, user_info)
        
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
    
    def _add_ditual_header(self, story: List, budget: Any):
        """Adiciona cabeçalho moderno e elegante da Ditual"""
        
        # Dados da empresa atualizados
        company_data = [
            [
                # Logo + Nome da empresa
                self._get_logo_cell(),
                # Informações da empresa
                Paragraph("""
                    <b>DITUAL SAO PAULO DISTRIBUIDORA DE TUBOS E ACOS\u00A0LTDA</b><br/>
                    CNPJ: 25.033.094/0001-26<br/>
                    Estr. Presidente Juscelino Kubitschek De Oliveira, 1996<br/>
                    Jardim Albertina - Guarulhos/SP - CEP: 07260-000<br/>
                    Telefone: (11) 2489-9110 | E-mail: vendas@ditualsp.com.br
                """, self.styles['CompanyInfo']),
                # Número da proposta
                Paragraph(f"Proposta: <b>{budget.order_number}</b>", 
                         self.styles['ProposalNumber'])
            ]
        ]
        
        # Larguras somando exatamente à largura útil (≈ 180 mm)
        header_table = Table(company_data, colWidths=[47*mm, 95*mm, 38*mm])
        header_table.setStyle(TableStyle([
            # Fundo branco moderno
            ('BACKGROUND', (0, 0), (-1, 0), self.HEADER_BG),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, 0), 10),
            ('RIGHTPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (2, 0), (2, 0), 'TOP'),
            # Borda sutil na parte inferior
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.BORDER_COLOR),
        ]))

        story.append(header_table)
        story.append(Spacer(1, 25))
    
    def _get_logo_cell(self):
        """Retorna célula com logo da empresa ou espaço reservado"""
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                # Ajustar tamanho do logo proporcionalmente
                img = Image(self.logo_path, width=45*mm, height=22*mm)
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
    
    def _add_client_info(self, story: List, budget: Any, user_info: Optional[UserInfo] = None):
        """Adiciona informações do cliente e proposta"""
        
        # Formatar data
        created_date = budget.created_at.strftime('%d/%m/%Y') if budget.created_at else datetime.now().strftime('%d/%m/%Y')
        expires_date = budget.expires_at.strftime('%d/%m/%Y') if budget.expires_at else "7 dias corridos"
        
        # Preparar informações do consultor
        consultant_name = budget.created_by or "Sistema"
        consultant_email = ""
        
        if user_info:
            # Capitalizar primeira letra do nome completo
            consultant_name = user_info.full_name.title() if user_info.full_name else user_info.username.title()
            consultant_email = user_info.email
        else:
            # Fallback: capitalizar apenas o username
            consultant_name = consultant_name.title()
        
        # Dados do cliente e proposta
        client_data = [
            [
                Paragraph("Cliente:", self.styles['ClientLabel']),
                Paragraph(budget.client_name.upper(), self.styles['ClientValue']),
                "",
                Paragraph("Consultor:", self.styles['ClientLabel']),
                Paragraph(consultant_name, self.styles['ClientValue'])
            ],
            [
                Paragraph("Data:", self.styles['ClientLabel']),
                Paragraph(created_date, self.styles['ClientValue']),
                "",
                Paragraph("E-mail:", self.styles['ClientLabel']),
                Paragraph(consultant_email, self.styles['ClientValue'])  # Email do consultor
            ],
            [
                Paragraph("Validade:", self.styles['ClientLabel']),
                Paragraph(expires_date, self.styles['ClientValue']),
                "",
                "",
                ""
            ]
        ]
        
        # Ajuste para 180 mm no total
        client_table = Table(client_data, colWidths=[24*mm, 66*mm, 8*mm, 26*mm, 56*mm])
        client_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
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
    
    def _add_items_table(self, story: List, budget: Any):
        """Adiciona tabela principal de itens (exatamente como na proposta)"""
        
        # Cabeçalho da tabela com títulos sem quebras de linha
        header_data = [
            [
                "Item",
                "Descrição", 
                "Und",
                "Qtd",
                "Preço Unit.",
                "ICMS",
                "IPI (%)",
                "Prazo"
            ]
        ]
        
        # Dados dos itens
        table_data = []
        for i, item in enumerate(budget.items, 1):
            # Calcular valores para exibição
            unit_price = item.sale_value_with_icms or item.unit_value or 0
            icms_percentage = item.sale_icms_percentage or 0
            
            # Formatação da QTD usando peso de venda com fallback para peso de compra
            qtd_weight = item.sale_weight if item.sale_weight is not None else (item.weight or 0.0)
            weight_str = f"{qtd_weight:,.0f}".replace(',', '.')
            unit_price_str = self._format_currency(unit_price)
            # Percentuais com vírgula (pt-BR)
            icms_str = (f"{icms_percentage * 100:.1f}".replace('.', ',') + '%')
            ipi_percent = (item.ipi_percentage or 0) * 100
            ipi_str = (f"{ipi_percent:.2f}".replace('.', ',') + '%')
            
            row_data = [
                str(i),
                Paragraph(item.description, self.styles['Normal']),
                "KG",
                weight_str,
                unit_price_str,
                icms_str,
                ipi_str,
                self._format_delivery_time(item.delivery_time)
            ]
            
            table_data.append(row_data)
        
        # Combinar cabeçalho e dados
        all_data = header_data + table_data
        
        # Larguras das colunas somando 180 mm
        col_widths = [14*mm, 62*mm, 12*mm, 18*mm, 28*mm, 14*mm, 14*mm, 18*mm]

        items_table = Table(all_data, colWidths=col_widths, repeatRows=1)
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
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            # Linhas alternadas para melhor leitura
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.DITUAL_LIGHT_GRAY]),
        ]))
        
        story.append(KeepTogether(items_table))
        story.append(Spacer(1, 5))
    
    def _add_totals_and_conditions(self, story: List, budget: Any):
        """Adiciona totais e peso (como na proposta)"""
        
        # Calcular totais
        total_weight = sum((item.sale_weight if item.sale_weight is not None else item.weight) for item in budget.items)
        
        # Valor Total S/IPI: soma dos valores de venda com ICMS (sem IPI)
        total_without_ipi = sum(
            (item.sale_value_with_icms or item.unit_value or 0) * (item.sale_weight if item.sale_weight is not None else item.weight)
            for item in budget.items
        )
        
        # Valor Total C/IPI: soma dos valores de venda com ICMS + IPI
        total_with_ipi = sum(
            ((item.sale_value_with_icms or item.unit_value or 0) * (item.sale_weight if item.sale_weight is not None else item.weight)) + (item.ipi_value or 0)
            for item in budget.items
        )
        
        # Tabela de totais moderna e elegante - Separando os valores IPI em linhas diferentes
        totals_data = [
            [
                Paragraph(f"Peso Total: {total_weight:,.0f} kg".replace(',', '.'), self.styles['ClientValue']),
                "",
                Paragraph(f"Valor total S/IPI: {self._format_currency(total_without_ipi)}", self.styles['ClientValue'])
            ],
            [
                "",
                "",
                Paragraph(f"Valor total C/IPI: {self._format_currency(total_with_ipi)}", self.styles['ClientValue'])
            ]
        ]

        totals_table = Table(totals_data, colWidths=[90*mm, 10*mm, 80*mm])
        totals_table.setStyle(TableStyle([
            # Estilo moderno para totais
            ('BACKGROUND', (0, 0), (-1, -1), self.DITUAL_LIGHT_GRAY),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.DITUAL_DARK_GRAY),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
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
        
        story.append(KeepTogether(totals_table))
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
        
        story.append(KeepTogether(obs_table))
        story.append(Spacer(1, 12))
    
    def _add_commercial_conditions(self, story: List, budget: Any):
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
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(KeepTogether(freight_table))
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
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(KeepTogether(payment_table))
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
        
        story.append(KeepTogether(legal_table))


class PDFExportService:
    """Serviço principal para exportação de PDF"""
    
    def __init__(self):
        self.template = DitualPDFTemplate()
    
    async def generate_proposal_pdf(self, budget: Any, auth_token: Optional[str] = None) -> bytes:
        """Gera PDF da proposta usando template oficial da Ditual"""
        return await self.template.generate_proposal_pdf(budget, auth_token)
    
    async def generate_simplified_proposal_pdf(self, budget: Any, auth_token: Optional[str] = None) -> bytes:
        """
        Mantido por compatibilidade, mas agora usa o mesmo template oficial
        """
        return await self.template.generate_proposal_pdf(budget, auth_token)


# Instância singleton do serviço
pdf_export_service = PDFExportService()

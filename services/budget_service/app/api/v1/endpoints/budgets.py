from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.budget import BudgetStatus
from app.schemas.budget import (
    BudgetCreate, BudgetUpdate, BudgetResponse, BudgetSummary, BudgetCalculation,
    BudgetSimplifiedCreate, MarkupConfiguration, BudgetItemCreate
)
from app.services.budget_service import BudgetService
from app.services.budget_calculator import BudgetCalculatorService
from app.services.pdf_export_service import pdf_export_service

router = APIRouter()


async def generate_order_number(db: AsyncSession) -> str:
    """Gera número sequencial do pedido no formato PED-0001"""
    from sqlalchemy import text
    
    # Buscar o último número de pedido
    result = await db.execute(
        text("SELECT order_number FROM budgets WHERE order_number LIKE 'PED-%' ORDER BY order_number DESC LIMIT 1")
    )
    last_order = result.scalar()
    
    if last_order:
        # Extrair número e incrementar
        try:
            last_number = int(last_order.split('-')[1])
            next_number = last_number + 1
        except (IndexError, ValueError):
            next_number = 1
    else:
        next_number = 1
    
    return f"PED-{next_number:04d}"


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    created_by: str = "admin"  # TODO: Get from JWT token
):
    """Criar um novo orçamento"""
    try:
        # Check if order number already exists
        existing_budget = await BudgetService.get_budget_by_order_number(db, budget_data.order_number)
        if existing_budget:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Número do pedido já existe"
            )
        
        budget = await BudgetService.create_budget(db, budget_data, created_by)
        
        # Get budget with items using eager loading to avoid MissingGreenlet error
        budget_with_items = await BudgetService.get_budget_by_id(db, budget.id)
        return budget_with_items
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[BudgetSummary])
async def get_budgets(
    skip: int = 0,
    limit: int = 100,
    status: Optional[BudgetStatus] = None,
    client_name: Optional[str] = None,
    created_by: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Listar orçamentos com filtros"""
    budgets = await BudgetService.get_budgets(
        db, skip=skip, limit=limit, status=status, 
        client_name=client_name, created_by=created_by
    )
    
    # Convert to summary format
    summaries = []
    for budget in budgets:
        summaries.append(BudgetSummary(
            id=budget.id,
            order_number=budget.order_number,
            client_name=budget.client_name,
            status=budget.status,
            total_sale_value=budget.total_sale_value,
            total_commission=budget.total_commission,
            profitability_percentage=budget.profitability_percentage,
            items_count=len(budget.items),
            created_at=budget.created_at
        ))
    
    return summaries


@router.get("/markup-settings", response_model=MarkupConfiguration)
async def get_markup_settings():
    """Obter configurações de markup do sistema"""
    return MarkupConfiguration(
        minimum_markup_percentage=20.0,
        maximum_markup_percentage=200.0,
        default_market_position="competitive",
        icms_sale_default=17.0,
        commission_default=1.5,
        other_expenses_default=0.0
    )


@router.get("/next-order-number")
async def get_next_order_number(db: AsyncSession = Depends(get_db)):
    """Obter o próximo número de pedido disponível"""
    next_number = await generate_order_number(db)
    return {"order_number": next_number}


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obter orçamento por ID"""
    budget = await BudgetService.get_budget_by_id(db, budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return budget


@router.get("/order/{order_number}", response_model=BudgetResponse)
async def get_budget_by_order(
    order_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Obter orçamento por número do pedido"""
    budget = await BudgetService.get_budget_by_order_number(db, order_number)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Atualizar orçamento"""
    budget = await BudgetService.update_budget(db, budget_id, budget_data)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Deletar orçamento"""
    success = await BudgetService.delete_budget(db, budget_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )


@router.post("/{budget_id}/recalculate", response_model=BudgetResponse)
async def recalculate_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Recalcular totais do orçamento"""
    budget = await BudgetService.recalculate_budget(db, budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return budget


@router.post("/{budget_id}/apply-markup", response_model=BudgetResponse)
async def apply_markup(
    budget_id: int,
    markup_percentage: float = Query(..., description="Markup percentage to apply"),
    db: AsyncSession = Depends(get_db)
):
    """Aplicar markup ao orçamento"""
    if markup_percentage < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Markup deve ser positivo"
        )
    
    budget = await BudgetService.apply_markup_to_budget(db, budget_id, markup_percentage)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return budget


@router.post("/calculate", response_model=BudgetCalculation)
async def calculate_budget(
    budget_data: BudgetCreate
):
    """Calcular orçamento sem salvar (preview)"""
    try:
        # Validate data
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_budget_data(budget_dict)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )
        
        # Calculate
        items_data = [item.dict() for item in budget_data.items]
        totals = BudgetCalculatorService.calculate_budget_totals(items_data)
        
        # Calculate each item
        items_calculations = []
        for item_data in items_data:
            calculations = BudgetCalculatorService.calculate_item_totals(item_data)
            items_calculations.append({
                'description': item_data['description'],
                'quantity': item_data['quantity'],
                'total_purchase': calculations['total_purchase'],
                'total_sale': calculations['total_sale'],
                'profitability': calculations['profitability'],
                'commission_value': calculations['commission_value']
            })
        
        return BudgetCalculation(
            total_purchase_value=totals['total_purchase_value'],
            total_sale_value=totals['total_sale_value'],
            total_commission=totals['total_commission'],
            profitability_percentage=totals['profitability_percentage'],
            markup_percentage=totals['markup_percentage'],
            items_calculations=items_calculations
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/calculate-with-markup", response_model=BudgetCalculation)
async def calculate_with_markup(
    budget_data: BudgetCreate,
    markup_percentage: float = Query(..., description="Desired markup percentage")
):
    """Calcular orçamento com markup específico (preview)"""
    try:
        if markup_percentage < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Markup deve ser positivo"
            )
        
        # Validate data
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_budget_data(budget_dict)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )
        
        # Calculate with markup
        items_data = [item.dict() for item in budget_data.items]
        result = BudgetCalculatorService.calculate_with_markup(items_data, markup_percentage)
        
        # Format items calculations
        items_calculations = []
        for item in result['adjusted_items']:
            items_calculations.append({
                'description': item['description'],
                'quantity': item['quantity'],
                'adjusted_sale_price': item['sale_value_with_icms'],
                'total_purchase': item['total_purchase'],
                'total_sale': item['total_sale'],
                'profitability': item['profitability'],
                'commission_value': item['commission_value']
            })
        
        return BudgetCalculation(
            total_purchase_value=result['totals']['total_purchase_value'],
            total_sale_value=result['totals']['total_sale_value'],
            total_commission=result['totals']['total_commission'],
            profitability_percentage=result['totals']['profitability_percentage'],
            markup_percentage=result['totals']['markup_percentage'],
            items_calculations=items_calculations
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/calculate-simplified", response_model=BudgetCalculation)
async def calculate_simplified_budget(
    budget_data: BudgetSimplifiedCreate
):
    """Calcular orçamento simplificado com apenas campos obrigatórios"""
    try:
        # Validar dados
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )
        
        # Calcular usando função simplificada
        calculation_result = BudgetCalculatorService.calculate_simplified_budget(budget_data.items)
        
        # Preparar resposta
        items_calculations = []
        for item in calculation_result['items']:
            items_calculations.append({
                'description': item['description'],
                'quantity': item['quantity'],
                'total_purchase': item['total_purchase'],
                'total_sale': item['total_sale'],
                'profitability': item['profitability'],
                'commission_value': item['commission_value']
            })
        
        return BudgetCalculation(
            total_purchase_value=calculation_result['totals']['total_purchase_value'],
            total_sale_value=calculation_result['totals']['total_sale_value'],
            total_commission=calculation_result['totals']['total_commission'],
            profitability_percentage=calculation_result['totals']['profitability_percentage'],
            markup_percentage=calculation_result['totals']['markup_percentage'],
            items_calculations=items_calculations
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/simplified", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_simplified_budget(
    budget_data: BudgetSimplifiedCreate,
    db: AsyncSession = Depends(get_db),
    created_by: str = "admin"  # TODO: Get from JWT token
):
    """Criar orçamento simplificado com geração automática de número do pedido"""
    try:
        # Validar dados de entrada
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )
        
        # Gerar número do pedido se não fornecido
        order_number = budget_data.order_number
        if not order_number:
            order_number = await generate_order_number(db)
        else:
            # Verificar se número do pedido já existe
            existing_budget = await BudgetService.get_budget_by_order_number(db, order_number)
            if existing_budget:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Número do pedido já existe"
                )
        
        # Calcular todos os valores baseados nos dados de entrada
        calculation_result = BudgetCalculatorService.calculate_simplified_budget(budget_data.items)
        
        # Criar orçamento completo para salvar
        complete_budget_data = BudgetCreate(
            order_number=order_number,
            client_name=budget_data.client_name,
            markup_percentage=calculation_result['totals']['markup_percentage'],
            notes=budget_data.notes,
            expires_at=budget_data.expires_at,
            items=[BudgetItemCreate(**item_data) for item_data in calculation_result['items']]
        )
        
        budget = await BudgetService.create_budget(db, complete_budget_data, created_by)
        
        # Retornar orçamento completo
        budget_with_items = await BudgetService.get_budget_by_id(db, budget.id)
        return budget_with_items
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/calculate-markup", response_model=dict)
async def calculate_item_markup(
    purchase_value_with_icms: float = Query(..., description="Valor de compra com ICMS"),
    purchase_icms_percentage: float = Query(..., description="Percentual de ICMS na compra"),
    sale_value_with_icms: float = Query(..., description="Valor de venda com ICMS"),
    sale_icms_percentage: float = Query(17.0, description="Percentual de ICMS na venda"),
    other_expenses: float = Query(0.0, description="Outras despesas")
):
    """
    Calcular markup automaticamente baseado nos valores de compra e venda
    Segue exatamente a fórmula da planilha de referência
    """
    try:
        markup_percentage = BudgetCalculatorService.calculate_automatic_markup_from_planilha(
            purchase_value_with_icms=purchase_value_with_icms,
            purchase_icms_percentage=purchase_icms_percentage,
            sale_value_with_icms=sale_value_with_icms,
            sale_icms_percentage=sale_icms_percentage,
            other_expenses=other_expenses
        )
        
        # Calcular valores sem impostos para referência
        purchase_without_taxes = purchase_value_with_icms * (1 - purchase_icms_percentage / 100)
        sale_without_taxes = sale_value_with_icms * (1 - sale_icms_percentage / 100)
        total_cost = purchase_without_taxes + other_expenses
        profit = sale_without_taxes - total_cost
        
        return {
            "success": True,
            "data": {
                "markup_percentage": markup_percentage,
                "breakdown": {
                    "purchase_value_with_icms": purchase_value_with_icms,
                    "purchase_value_without_taxes": round(purchase_without_taxes, 2),
                    "other_expenses": other_expenses,
                    "total_cost": round(total_cost, 2),
                    "sale_value_with_icms": sale_value_with_icms,
                    "sale_value_without_taxes": round(sale_without_taxes, 2),
                    "profit": round(profit, 2),
                    "markup_percentage": markup_percentage
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no cálculo do markup: {str(e)}"
        )


@router.post("/suggest-sale-price", response_model=dict)
async def suggest_sale_price_from_markup(
    purchase_value_with_icms: float = Query(..., description="Valor de compra com ICMS"),
    purchase_icms_percentage: float = Query(..., description="Percentual de ICMS na compra"),
    desired_markup_percentage: float = Query(..., description="Markup desejado em percentual"),
    sale_icms_percentage: float = Query(17.0, description="Percentual de ICMS na venda"),
    other_expenses: float = Query(0.0, description="Outras despesas")
):
    """
    Sugerir preço de venda necessário para atingir um markup desejado
    Baseado na fórmula inversa da planilha
    """
    try:
        suggested_sale_price = BudgetCalculatorService.calculate_sale_price_from_markup(
            purchase_value_with_icms=purchase_value_with_icms,
            purchase_icms_percentage=purchase_icms_percentage,
            sale_icms_percentage=sale_icms_percentage,
            desired_markup_percentage=desired_markup_percentage,
            other_expenses=other_expenses
        )
        
        # Verificar se o markup calculado realmente bate
        actual_markup = BudgetCalculatorService.calculate_automatic_markup_from_planilha(
            purchase_value_with_icms=purchase_value_with_icms,
            purchase_icms_percentage=purchase_icms_percentage,
            sale_value_with_icms=suggested_sale_price,
            sale_icms_percentage=sale_icms_percentage,
            other_expenses=other_expenses
        )
        
        # Calcular valores para referência
        purchase_without_taxes = purchase_value_with_icms * (1 - purchase_icms_percentage / 100)
        sale_without_taxes = suggested_sale_price * (1 - sale_icms_percentage / 100)
        total_cost = purchase_without_taxes + other_expenses
        profit = sale_without_taxes - total_cost
        
        return {
            "success": True,
            "data": {
                "suggested_sale_price": suggested_sale_price,
                "actual_markup_achieved": actual_markup,
                "breakdown": {
                    "purchase_value_with_icms": purchase_value_with_icms,
                    "purchase_value_without_taxes": round(purchase_without_taxes, 2),
                    "other_expenses": other_expenses,
                    "total_cost": round(total_cost, 2),
                    "suggested_sale_price": suggested_sale_price,
                    "sale_value_without_taxes": round(sale_without_taxes, 2),
                    "profit": round(profit, 2),
                    "desired_markup": desired_markup_percentage,
                    "actual_markup": actual_markup
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no cálculo do preço de venda: {str(e)}"
        )


@router.get("/{budget_id}/export-pdf")
async def export_budget_as_pdf(
    budget_id: int,
    simplified: bool = Query(False, description="Gerar versão simplificada da proposta"),
    db: AsyncSession = Depends(get_db)
):
    """Exportar orçamento como proposta em PDF"""
    try:
        # Buscar orçamento
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        # Gerar PDF
        if simplified:
            pdf_content = pdf_export_service.generate_simplified_proposal_pdf(budget)
            filename = f"Proposta_Simplificada_{budget.order_number}.pdf"
        else:
            pdf_content = pdf_export_service.generate_proposal_pdf(budget)
            filename = f"Proposta_Completa_{budget.order_number}.pdf"
        
        # Retornar PDF como resposta
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar PDF: {str(e)}"
        )


@router.get("/order/{order_number}/export-pdf")
async def export_budget_by_order_as_pdf(
    order_number: str,
    simplified: bool = Query(False, description="Gerar versão simplificada da proposta"),
    db: AsyncSession = Depends(get_db)
):
    """Exportar orçamento como proposta em PDF usando número do pedido"""
    try:
        # Buscar orçamento por número do pedido
        budget = await BudgetService.get_budget_by_order_number(db, order_number)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        # Gerar PDF
        if simplified:
            pdf_content = pdf_export_service.generate_simplified_proposal_pdf(budget)
            filename = f"Proposta_Simplificada_{budget.order_number}.pdf"
        else:
            pdf_content = pdf_export_service.generate_proposal_pdf(budget)
            filename = f"Proposta_Completa_{budget.order_number}.pdf"
        
        # Retornar PDF como resposta
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar PDF: {str(e)}"
        )

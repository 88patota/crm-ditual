from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.budget import BudgetStatus
from app.schemas.budget import (
    BudgetCreate, BudgetUpdate, BudgetResponse, BudgetSummary, BudgetCalculation
)
from app.services.budget_service import BudgetService
from app.services.budget_calculator import BudgetCalculatorService

router = APIRouter()


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
        return budget
        
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
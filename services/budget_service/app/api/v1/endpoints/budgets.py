from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_active_user, get_user_filter, require_admin, CurrentUser
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
    current_user: CurrentUser = Depends(get_current_active_user)
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
        
        budget = await BudgetService.create_budget(db, budget_data, current_user.username)
        
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
    days: Optional[int] = Query(None, description="Filtro de dias (1=hoje, 3, 7, 15, 30)"),
    custom_start: Optional[str] = Query(None, description="Data inicial customizada (YYYY-MM-DD)"),
    custom_end: Optional[str] = Query(None, description="Data final customizada (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    user_filter: Optional[str] = Depends(get_user_filter)
):
    """Listar orçamentos com filtros baseados no perfil do usuário"""
    
    # Se user_filter não é None, significa que é um vendedor e deve ver apenas seus orçamentos
    if user_filter is not None:
        created_by = user_filter
    
    budgets = await BudgetService.get_budgets(
        db, skip=skip, limit=limit, status=status, 
        client_name=client_name, created_by=created_by,
        days=days, custom_start=custom_start, custom_end=custom_end
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
            total_sale_with_icms=budget.total_sale_with_icms or 0.0,
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


@router.get("/test-debug")
async def test_debug_endpoint():
    """Endpoint simples para testar se o debug está funcionando"""
    return {"message": "Debug endpoint is working!", "timestamp": "2025-09-15"}


@router.get("/debug-delivery/{budget_id}")
async def debug_budget_delivery_time(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """DEBUG: Verificar delivery_time diretamente do banco"""
    try:
        from sqlalchemy import text
        
        # Query direta no banco
        result = await db.execute(text(
            "SELECT id, description, delivery_time FROM budget_items WHERE budget_id = :budget_id"
        ), {"budget_id": budget_id})
        
        items = []
        for row in result:
            items.append({
                "id": row[0],
                "description": row[1],
                "delivery_time_raw": row[2],
                "delivery_time_repr": repr(row[2])
            })
        
        return {"budget_id": budget_id, "items": items, "status": "success"}
    except Exception as e:
        return {"budget_id": budget_id, "error": str(e), "status": "error"}


@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Obter orçamento por ID com controle de acesso"""
    budget = await BudgetService.get_budget_by_id(db, budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    
    # Verificar se o usuário tem permissão para ver este orçamento
    if current_user.role != "admin" and budget.created_by != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: você só pode visualizar seus próprios orçamentos"
        )
    
    # DEBUG: Log delivery_time before returning
    if budget.items:
        print(f"🔍 DEBUG - GET endpoint returning budget {budget_id}:")
        for i, item in enumerate(budget.items):
            print(f"🔍 DEBUG - Item {i}: delivery_time before response = {repr(item.delivery_time)}")
    
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
        from app.services.business_rules_calculator import BusinessRulesCalculator

        # Validate data
        budget_dict = budget_data.dict()
        errors = BudgetCalculatorService.validate_budget_data(budget_dict)
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )

        # Convert items to BusinessRulesCalculator format
        items_data = []
        total_peso_pedido = 0.0

        for item in budget_data.items:
            item_dict = item.dict()
            # Convert field names to Portuguese format expected by BusinessRulesCalculator
            converted_item = {
                'description': item_dict.get('description', ''),
                'peso_compra': item_dict.get('weight', 1.0),
                'peso_venda': item_dict.get('sale_weight', item_dict.get('weight', 1.0)),
                'valor_com_icms_compra': item_dict.get('purchase_value_with_icms', 0),
                'percentual_icms_compra': item_dict.get('purchase_icms_percentage', 0.18),
                'outras_despesas_item': item_dict.get('purchase_other_expenses', 0),
                'valor_com_icms_venda': item_dict.get('sale_value_with_icms', 0),
                'percentual_icms_venda': item_dict.get('sale_icms_percentage', 0.17),
                'percentual_ipi': item_dict.get('ipi_percentage', 0.0),
                'dunamis_cost': item_dict.get('dunamis_cost')
            }
            total_peso_pedido += converted_item['peso_compra']
            items_data.append(converted_item)

        # Validate items using business rules
        for i, item_data in enumerate(items_data):
            errors = BusinessRulesCalculator.validate_item_data(item_data)
            if errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Item {i+1}: {'; '.join(errors)}"
                )

        # Calculate using BusinessRulesCalculator
        outras_despesas_totais = sum(item.get('purchase_other_expenses', 0) for item in items_data)

        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, total_peso_pedido
        )

        calculated_items = budget_result['items']
        total_purchase_value = budget_result['totals']['soma_total_compra']
        total_sale_value = budget_result['totals']['soma_total_venda']
        total_sale_with_icms = budget_result['totals']['soma_total_venda_com_icms']
        total_commission = budget_result['totals']['total_comissao']
        total_ipi_value = budget_result['totals']['total_ipi_orcamento']
        total_final_value = budget_result['totals']['total_final_com_ipi']

        # Calculate taxes
        total_net_revenue = total_sale_value
        total_taxes = total_sale_with_icms - total_net_revenue

        # Calculate markup
        markup_percentage = budget_result['totals']['markup_pedido']
        profitability_percentage = markup_percentage

        # Prepare response
        items_calculations = []
        for item in calculated_items:
            items_calculations.append({
                'description': item['description'],
                'weight': item['peso_compra'],
                'total_purchase': item['total_compra_item'],
                'total_sale': item['total_venda_item'],
                'profitability': item['rentabilidade_item'] * 100,
                'commission_value': item['valor_comissao'],
                'ipi_percentage': item['percentual_ipi'],
                'ipi_value': item['valor_ipi_total'],
                'total_value_with_ipi': item['total_final_com_ipi']
            })

        return BudgetCalculation(
            total_purchase_value=round(total_purchase_value, 2),
            total_sale_value=round(total_sale_value, 2),
            total_net_revenue=round(total_net_revenue, 2),
            total_taxes=round(total_taxes, 2),
            total_commission=round(total_commission, 2),
            profitability_percentage=round(profitability_percentage, 2),
            markup_percentage=round(markup_percentage, 2),
            items_calculations=items_calculations,
            total_ipi_value=round(total_ipi_value, 2),
            total_final_value=round(total_final_value, 2)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no cálculo: {str(e)}"
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
                'weight': item.get('weight', 1.0),
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
    """Calcular orçamento simplificado usando business rules calculator"""
    try:
        from app.services.business_rules_calculator import BusinessRulesCalculator
        
        # Converter dados para formato esperado pelo BusinessRulesCalculator
        items_data = []
        total_peso_pedido = 0.0
        
        for item in budget_data.items:
            item_dict = item.dict()
            total_peso_pedido += item_dict.get('peso_compra', 1.0)
            items_data.append(item_dict)
        
        # Validar dados usando business rules
        for i, item_data in enumerate(items_data):
            errors = BusinessRulesCalculator.validate_item_data(item_data)
            if errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Item {i+1}: {'; '.join(errors)}"
                )
        
        # Calcular usando BusinessRulesCalculator
        outras_despesas_totais = 0.0  # Pode ser adicionado ao schema se necessário
        
        # Calcular orçamento completo usando BusinessRulesCalculator
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, total_peso_pedido
        )
        
        calculated_items = budget_result['items']
        total_purchase_value = budget_result['totals']['soma_total_compra']
        total_sale_value = budget_result['totals']['soma_total_venda']  # SEM impostos
        total_sale_with_icms = budget_result['totals']['soma_total_venda_com_icms']  # COM ICMS
        total_commission = budget_result['totals']['total_comissao']
        total_ipi_value = budget_result['totals']['total_ipi_orcamento']  # Total IPI
        total_final_value = budget_result['totals']['total_final_com_ipi']  # Valor final com IPI
        
        # Calcular impostos totais usando valores COM ICMS
        total_net_revenue = total_sale_value  # SEM impostos
        total_taxes = total_sale_with_icms - total_net_revenue
        
        # Calcular markup
        markup_percentage = budget_result['totals']['markup_pedido']
        profitability_percentage = markup_percentage
        
        # Preparar resposta
        items_calculations = []
        for item in calculated_items:
            items_calculations.append({
                'description': item['description'],
                'peso_compra': item['peso_compra'],
                'peso_venda': item['peso_venda'],
                'total_purchase': item['total_compra_item'],
                'total_sale': item['total_venda_item'],
                'profitability': item['rentabilidade_item'] * 100,  # Converter para percentual
                'commission_value': item['valor_comissao'],
                'commission_percentage_actual': item['commission_percentage_actual'],  # Actual percentage used
                # IPI fields
                'ipi_percentage': item['percentual_ipi'],
                'ipi_value': item['valor_ipi_total'],
                'total_value_with_ipi': item['total_final_com_ipi']
            })
        
        return BudgetCalculation(
            total_purchase_value=round(total_purchase_value, 2),
            total_sale_value=round(total_sale_value, 2),  # SEM impostos - muda quando ICMS muda
            total_net_revenue=round(total_net_revenue, 2),  # SEM impostos (mesmo que total_sale_value)
            total_taxes=round(total_taxes, 2),  # Impostos totais
            total_commission=round(total_commission, 2),
            profitability_percentage=round(profitability_percentage, 2),
            markup_percentage=round(markup_percentage, 2),
            items_calculations=items_calculations,
            # IPI calculations
            total_ipi_value=round(total_ipi_value, 2),
            total_final_value=round(total_final_value, 2)
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no cálculo: {str(e)}"
        )


@router.post("/simplified", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_simplified_budget(
    budget_data: BudgetSimplifiedCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
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
        
        # Usar BusinessRulesCalculator para calcular valores corretos
        from app.services.business_rules_calculator import BusinessRulesCalculator
        
        # Converter dados para formato do BusinessRulesCalculator
        items_data = [item.dict() for item in budget_data.items]
        soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in items_data)
        outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in items_data)
        
        # Calcular usando BusinessRulesCalculator
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, soma_pesos_pedido
        )
        
        # Converter resultados para formato BudgetItemCreate
        items_for_creation = []
        for calculated_item in budget_result['items']:
            items_for_creation.append(BudgetItemCreate(
                description=calculated_item['description'],
                weight=calculated_item['peso_compra'],
                delivery_time=calculated_item.get('delivery_time', '0'),  # CORREÇÃO: Incluir delivery_time
                purchase_value_with_icms=calculated_item['valor_com_icms_compra'],
                purchase_icms_percentage=calculated_item['percentual_icms_compra'],
                purchase_other_expenses=calculated_item['outras_despesas_distribuidas'],
                purchase_value_without_taxes=calculated_item['valor_sem_impostos_compra'],
                purchase_value_with_weight_diff=calculated_item.get('valor_corrigido_peso'),
                sale_weight=calculated_item['peso_venda'],
                sale_value_with_icms=calculated_item['valor_com_icms_venda'],
                sale_icms_percentage=calculated_item['percentual_icms_venda'],
                sale_value_without_taxes=calculated_item['valor_sem_impostos_venda'],
                weight_difference=calculated_item.get('diferenca_peso'),
                ipi_percentage=calculated_item['percentual_ipi'],  # CORREÇÃO: Incluir IPI percentage
                commission_percentage=0  # Será calculado pela rentabilidade
            ))
        
        # Criar orçamento completo para salvar
        complete_budget_data = BudgetCreate(
            order_number=order_number,
            client_name=budget_data.client_name,
            markup_percentage=budget_result['totals']['markup_pedido'],
            notes=budget_data.notes,
            expires_at=budget_data.expires_at,
            # CORREÇÃO: Incluir campos prazo_medio e outras_despesas_totais
            prazo_medio=budget_data.prazo_medio,
            outras_despesas_totais=budget_data.outras_despesas_totais,
            items=items_for_creation
        )
        
        budget = await BudgetService.create_budget(db, complete_budget_data, current_user.username)
        
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
    Segue exatamente as regras de negócio definidas (incluindo PIS/COFINS)
    """
    try:
        markup_percentage = BudgetCalculatorService.calculate_automatic_markup_from_planilha(
            purchase_value_with_icms=purchase_value_with_icms,
            purchase_icms_percentage=purchase_icms_percentage,
            sale_value_with_icms=sale_value_with_icms,
            sale_icms_percentage=sale_icms_percentage,
            other_expenses=other_expenses
        )
        
        # Calcular valores conforme regras 1 e 3 (incluindo PIS/COFINS)
        purchase_without_taxes = (purchase_value_with_icms * (1 - purchase_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        sale_without_taxes = (sale_value_with_icms * (1 - sale_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        total_cost = purchase_without_taxes + other_expenses
        profit = sale_without_taxes - total_cost
        
        # Calcular custo Dunamis conforme regra 10
        dunamis_cost = BudgetCalculatorService.calculate_dunamis_cost(
            purchase_value_with_icms=purchase_value_with_icms,
            sale_icms_percentage=sale_icms_percentage
        )
        
        return {
            "success": True,
            "data": {
                "markup_percentage": markup_percentage,
                "breakdown": {
                    "valor_com_icms_compra": purchase_value_with_icms,
                    "purchase_value_without_taxes": round(purchase_without_taxes, 6),
                    "other_expenses": other_expenses,
                    "total_cost": round(total_cost, 6),
                    "valor_com_icms_venda": sale_value_with_icms,
                    "sale_value_without_taxes": round(sale_without_taxes, 6),
                    "profit": round(profit, 6),
                    "markup_percentage": markup_percentage,
                    "dunamis_cost": round(dunamis_cost, 6),
                    "pis_cofins_percentage": BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE
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
    Baseado nas regras de negócio atualizadas (incluindo PIS/COFINS)
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
        
        # Calcular valores conforme regras 1 e 3 (incluindo PIS/COFINS)
        purchase_without_taxes = (purchase_value_with_icms * (1 - purchase_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        sale_without_taxes = (suggested_sale_price * (1 - sale_icms_percentage / 100)) * (1 - BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE / 100)
        total_cost = purchase_without_taxes + other_expenses
        profit = sale_without_taxes - total_cost
        
        # Calcular custo Dunamis também para referência
        dunamis_cost = BudgetCalculatorService.calculate_dunamis_cost(
            purchase_value_with_icms=purchase_value_with_icms,
            sale_icms_percentage=sale_icms_percentage
        )
        
        return {
            "success": True,
            "data": {
                "suggested_sale_price": round(suggested_sale_price, 2),
                "actual_markup_achieved": round(actual_markup, 2),
                "breakdown": {
                    "purchase_value_with_icms": purchase_value_with_icms,
                    "purchase_value_without_taxes": round(purchase_without_taxes, 6),
                    "other_expenses": other_expenses,
                    "total_cost": round(total_cost, 6),
                    "suggested_sale_price": round(suggested_sale_price, 2),
                    "sale_value_without_taxes": round(sale_without_taxes, 6),
                    "profit": round(profit, 6),
                    "desired_markup": desired_markup_percentage,
                    "actual_markup": round(actual_markup, 2),
                    "dunamis_cost": round(dunamis_cost, 6),
                    "pis_cofins_percentage": BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no cálculo do preço de venda: {str(e)}"
        )


@router.post("/calculate-dunamis-cost", response_model=dict)
async def calculate_dunamis_cost(
    purchase_value_with_icms: float = Query(..., description="Valor de compra com ICMS"),
    sale_icms_percentage: float = Query(17.0, description="Percentual de ICMS na venda"),
    weight: float = Query(1.0, description="Peso do item")
):
    """
    Calcular custo a ser lançado no Dunamis conforme Regra 10
    Fórmula: Valor c/ICMS (Compra) / (1 - %ICMS (Venda)) / (1 - Taxa PIS/COFINS)
    """
    try:
        dunamis_cost_unit = BudgetCalculatorService.calculate_dunamis_cost(
            purchase_value_with_icms=purchase_value_with_icms,
            sale_icms_percentage=sale_icms_percentage
        )
        
        dunamis_cost_total = dunamis_cost_unit * weight
        
        return {
            "success": True,
            "data": {
                "dunamis_cost_per_unit": round(dunamis_cost_unit, 6),
                "dunamis_cost_total": round(dunamis_cost_total, 6),
                "calculation_details": {
                    "purchase_value_with_icms": purchase_value_with_icms,
                    "sale_icms_percentage": sale_icms_percentage,
                    "pis_cofins_percentage": BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE,
                                        "formula": "Valor Compra c/ICMS / (1 - %ICMS Venda) / (1 - %PIS/COFINS)",
                    "step1": f"{purchase_value_with_icms} / (1 - {sale_icms_percentage}%)",
                    "step2": f"/ (1 - {BudgetCalculatorService.DEFAULT_PIS_COFINS_PERCENTAGE}%)",
                    "result_per_unit": round(dunamis_cost_unit, 6)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no cálculo do custo Dunamis: {str(e)}"
        )


@router.get("/{budget_id}/export-pdf")
async def export_budget_as_pdf(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Exportar orçamento como proposta em PDF usando template oficial da Ditual"""
    try:
        # Buscar orçamento
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        # Verificar permissão
        if current_user.role != "admin" and budget.created_by != current_user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado: você só pode exportar seus próprios orçamentos"
            )
        
        # Gerar PDF usando template oficial
        pdf_content = pdf_export_service.generate_proposal_pdf(budget)
        filename = f"Proposta_{budget.order_number}.pdf"
        
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
    db: AsyncSession = Depends(get_db)
):
    """Exportar orçamento como proposta em PDF pelo número do pedido"""
    try:
        # Buscar orçamento por número do pedido
        budget = await BudgetService.get_budget_by_order_number(db, order_number)
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        # Gerar PDF usando template oficial
        pdf_content = pdf_export_service.generate_proposal_pdf(budget)
        filename = f"Proposta_{budget.order_number}.pdf"
        
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

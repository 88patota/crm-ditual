from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_active_user, get_user_filter, require_admin, CurrentUser
from app.models.budget import BudgetStatus
from app.schemas.budget import (
    BudgetCreate, BudgetUpdate, BudgetResponse, BudgetSummary, BudgetCalculation,
    BudgetSimplifiedCreate, BudgetItemCreate
)
from app.services.budget_service import BudgetService
from app.services.budget_calculator import BudgetCalculatorService
from app.services.pdf_export_service import pdf_export_service
from app.utils.rounding import round_currency, round_percent, round_percent_display
import logging

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


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
            commission_percentage_actual=budget.commission_percentage_actual if budget.commission_percentage_actual is not None else 0.0,
            items_count=len(budget.items),
            created_at=budget.created_at
        ))
    
    return summaries


# Removido: endpoint de configurações de markup


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
    """Obter orçamento por ID"""
    try:
        budget = await BudgetService.get_budget_by_id(db, budget_id)
        
        if not budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        logger.debug(f"Budget {budget_id} retrieved successfully")
        
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
    except Exception as e:
        logger.error(f"Error retrieving budget {budget_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


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
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Atualizar orçamento"""
    try:
        logger.debug(f"Updating budget {budget_id}")
        
        updated_budget = await BudgetService.update_budget(db, budget_id, budget_data)
        
        if not updated_budget:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        logger.info(f"Budget {budget_id} updated successfully")
        return updated_budget
    except Exception as e:
        logger.error(f"Error updating budget {budget_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


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


# Removido: endpoint de aplicação de markup ao orçamento


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
            total_peso_pedido += converted_item['peso_compra']  # CORREÇÃO: Usar peso_compra para distribuição do frete
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

        # Calcular rentabilidade para comissão (SEM ICMS)
        profitability_percentage = budget_result['totals']['markup_pedido_sem_impostos']

        # Prepare response
        items_calculations = []
        for item in calculated_items:
            items_calculations.append({
                'description': item['description'],
                'weight': item['peso_compra'],
                'total_purchase': item['total_compra_item'],
                'total_sale': item['total_venda_item'],
                'profitability': round_percent_display((item['rentabilidade_item'] or 0), 2),  # Conversão para % com HALF_UP
                'rentabilidade_comissao': round_percent_display((item.get('rentabilidade_comissao', 0.0) or 0), 2),
                'commission_value': item['valor_comissao'],
                'ipi_percentage': item['percentual_ipi'],
                'ipi_value': item['valor_ipi_total'],
                'total_value_with_ipi': item['total_final_com_ipi']
            })

        return BudgetCalculation(
            total_purchase_value=round_currency(total_purchase_value),
            total_sale_value=round_currency(total_sale_value),
            total_net_revenue=round_currency(total_net_revenue),
            total_taxes=round_currency(total_taxes),
            total_commission=round_currency(total_commission),
            profitability_percentage=round_percent_display(profitability_percentage, 2),  # SEM ICMS
            rentabilidade_comissao_total=round_percent_display(budget_result['totals']['markup_pedido_sem_impostos'], 2),
            items_calculations=items_calculations,
            total_ipi_value=round_currency(total_ipi_value),
            total_final_value=round_currency(total_final_value)
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


# Removido: endpoint de cálculo com markup específico (preview)


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
            # CORREÇÃO: Usar peso_compra para distribuição do frete, pois frete é custo de compra
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
        # CORREÇÃO: Não somar outras_despesas_item como despesas totais
        # pois cada item já tem suas próprias outras despesas definidas
        outras_despesas_totais = 0.0  # Não há despesas adicionais a distribuir
        
        # Calcular orçamento completo usando BusinessRulesCalculator
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, total_peso_pedido, budget_data.freight_value_total or 0.0
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
        
        # Calcular rentabilidade para comissão (SEM ICMS) em percentual
        profitability_percentage = budget_result['totals']['markup_pedido_sem_impostos'] * 100  # SEM ICMS
        
        # Calcular percentual de comissão real baseado no total de comissão e valor de venda
        commission_percentage_actual = 0.0
        if total_sale_value > 0:
            commission_percentage_actual = (total_commission / total_sale_value) * 100
        
        # Preparar resposta
        items_calculations = []
        for item in calculated_items:
            items_calculations.append({
                'description': item['description'],
                'peso_compra': item['peso_compra'],
                'peso_venda': item['peso_venda'],
                'total_purchase': item['total_compra_item'],
                'total_sale': item['total_venda_item'],
                'profitability': round_percent_display((item['rentabilidade_item'] or 0), 2),  # Converter para percentual com HALF_UP
                'rentabilidade_comissao': round_percent_display((item.get('rentabilidade_comissao', 0.0) or 0), 2),
                'commission_value': item['valor_comissao'],
                'commission_percentage_actual': item.get('commission_percentage_actual', 0.0),  # Actual percentage used
                # IPI fields
                'ipi_percentage': item['percentual_ipi'],
                'ipi_value': item['valor_ipi_total'],
                'total_value_with_ipi': item['total_final_com_ipi'],
                # Weight difference display
                'weight_difference_display': item.get('weight_difference_display')
            })
        
        return BudgetCalculation(
            total_purchase_value=round_currency(total_purchase_value),
            total_sale_value=round_currency(total_sale_value),  # SEM impostos - muda quando ICMS muda
            total_net_revenue=round_currency(total_net_revenue),  # SEM impostos (mesmo que total_sale_value)
            total_taxes=round_currency(total_taxes),  # Impostos totais
            total_commission=round_currency(total_commission),
            commission_percentage_actual=round_percent(commission_percentage_actual, 2),  # Campo obrigatório
            profitability_percentage=round_percent(profitability_percentage, 2),  # SEM ICMS
            rentabilidade_comissao_total=round_percent(profitability_percentage, 2),
            items_calculations=items_calculations,
            # IPI calculations
            total_ipi_value=round_currency(total_ipi_value),
            total_final_value=round_currency(total_final_value),
            # Weight difference
            total_weight_difference_percentage=round_percent(budget_result['totals']['total_weight_difference_percentage'], 2)
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


@router.put("/simplified/{budget_id}", response_model=BudgetResponse)
async def update_simplified_budget(
    budget_id: int,
    budget_data: BudgetSimplifiedCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Atualizar orçamento simplificado"""
    try:
        logger.info(f"🔧 [UPDATE DEBUG] Starting update for budget {budget_id}")
        logger.info(f"🔧 [UPDATE DEBUG] User: {current_user.username}")
        
        # Log incoming data
        budget_dict = budget_data.dict()
        logger.info(f"🔧 [UPDATE DEBUG] Received data keys: {list(budget_dict.keys())}")
        logger.info(f"🔧 [UPDATE DEBUG] Items count: {len(budget_dict.get('items', []))}")
        
        # Log each item's critical fields
        for i, item in enumerate(budget_dict.get('items', [])):
            logger.info(f"🔧 [UPDATE DEBUG] Item {i}: description='{item.get('description', 'N/A')}', "
                       f"peso_compra={item.get('peso_compra', 'N/A')}, "
                       f"valor_com_icms_compra={item.get('valor_com_icms_compra', 'N/A')}, "
                       f"valor_com_icms_venda={item.get('valor_com_icms_venda', 'N/A')}, "
                       f"percentual_ipi={item.get('percentual_ipi', 'N/A')}")
        
        # Validar dados de entrada
        logger.debug(f"🔧 [UPDATE DEBUG] Validating budget data...")
        errors = BudgetCalculatorService.validate_simplified_budget_data(budget_dict)
        if errors:
            logger.error(f"🔧 [UPDATE DEBUG] Validation errors: {errors}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados inválidos: {'; '.join(errors)}"
            )
        logger.info(f"🔧 [UPDATE DEBUG] Validation passed successfully")
        
        # Verificar se o orçamento existe
        logger.debug(f"🔧 [UPDATE DEBUG] Checking if budget {budget_id} exists...")
        existing_budget = await BudgetService.get_budget_by_id(db, budget_id)
        if not existing_budget:
            logger.error(f"🔧 [UPDATE DEBUG] Budget {budget_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        logger.info(f"🔧 [UPDATE DEBUG] Found existing budget: order_number={existing_budget.order_number}, "
                   f"client_name='{existing_budget.client_name}', items_count={len(existing_budget.items)}")
        
        # Verificar se o número do pedido já existe em outro orçamento
        if budget_data.order_number and budget_data.order_number != existing_budget.order_number:
            logger.debug(f"🔧 [UPDATE DEBUG] Checking order number uniqueness: {budget_data.order_number}")
            existing_order = await BudgetService.get_budget_by_order_number(db, budget_data.order_number)
            if existing_order and existing_order.id != budget_id:
                logger.error(f"🔧 [UPDATE DEBUG] Order number {budget_data.order_number} already exists in budget {existing_order.id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Número do pedido já existe em outro orçamento"
                )
        
        # Log data being sent to service
        logger.info(f"🔧 [UPDATE DEBUG] Calling BudgetService.update_budget_simplified...")
        logger.debug(f"🔧 [UPDATE DEBUG] Budget data summary: client_name='{budget_dict.get('client_name')}', "
                    f"order_number='{budget_dict.get('order_number')}', "
                    f"freight_type='{budget_dict.get('freight_type')}', "
                    f"prazo_medio={budget_dict.get('prazo_medio')}")
        
        # Usar o método update_budget_simplified do BudgetService
        updated_budget = await BudgetService.update_budget_simplified(db, budget_id, budget_dict)
        
        if not updated_budget:
            logger.error(f"🔧 [UPDATE DEBUG] BudgetService returned None for budget {budget_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orçamento não encontrado"
            )
        
        logger.info(f"🔧 [UPDATE DEBUG] Budget {budget_id} updated successfully")
        logger.info(f"🔧 [UPDATE DEBUG] Updated budget: order_number={updated_budget.order_number}, "
                   f"client_name='{updated_budget.client_name}', "
                   f"items_count={len(updated_budget.items)}, "
                   f"total_sale_value={updated_budget.total_sale_value}")
        
        return updated_budget
        
    except ValueError as e:
        logger.error(f"🔧 [UPDATE DEBUG] ValueError in budget {budget_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        # Re-raise HTTP exceptions without modification
        raise
    except Exception as e:
        logger.error(f"🔧 [UPDATE DEBUG] Unexpected error updating budget {budget_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )


@router.post("/simplified", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
async def create_simplified_budget(
    budget_data: BudgetSimplifiedCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Criar orçamento simplificado com geração automática de número do pedido"""
    try:
        # Campo PRAZO (delivery_time) corrigido - dados chegam corretamente
        
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
        
        # 🔍 DEBUG: Log items_data após conversão
        print(f"🔍 DEBUG - Items data após conversão:")
        for i, item_data in enumerate(items_data):
            print(f"🔍 DEBUG - Item {i}: delivery_time = {repr(item_data.get('delivery_time'))}")
        
        # CORREÇÃO: Usar peso_compra para distribuir frete (não peso_venda)
        soma_pesos_pedido = sum(item.get('peso_compra', 0) for item in items_data)
        outras_despesas_totais = sum(item.get('outras_despesas_item', 0) for item in items_data)
        
        # Calcular usando BusinessRulesCalculator
        budget_result = BusinessRulesCalculator.calculate_complete_budget(
            items_data, outras_despesas_totais, soma_pesos_pedido
        )
        
        # Converter resultados para formato BudgetItemCreate
        items_for_creation = []
        for i, calculated_item in enumerate(budget_result['items']):
            # Obter delivery_time do item original
            original_item = items_data[i] if i < len(items_data) else {}
            delivery_time_value = original_item.get('delivery_time', '0')
            
            # 🔍 DEBUG: Log delivery_time antes de criar BudgetItemCreate
            print(f"🔍 DEBUG - Item {i} antes de BudgetItemCreate:")
            print(f"🔍 DEBUG - original_item: {original_item}")
            print(f"🔍 DEBUG - delivery_time_value: {repr(delivery_time_value)}")
            
            budget_item = BudgetItemCreate(
                description=calculated_item['description'],
                weight=calculated_item['peso_compra'],
                delivery_time=delivery_time_value,  # Usar delivery_time do item original
                purchase_value_with_icms=calculated_item['valor_com_icms_compra'],
                purchase_icms_percentage=calculated_item['percentual_icms_compra'],
                purchase_other_expenses=calculated_item['outras_despesas_item'],
                purchase_value_without_taxes=calculated_item['valor_sem_impostos_compra'],
                purchase_value_with_weight_diff=calculated_item.get('valor_corrigido_peso'),
                sale_weight=calculated_item['peso_venda'],
                sale_value_with_icms=calculated_item['valor_com_icms_venda'],
                sale_icms_percentage=calculated_item['percentual_icms_venda'],
                sale_value_without_taxes=calculated_item['valor_sem_impostos_venda'],
                weight_difference=calculated_item.get('diferenca_peso'),
                ipi_percentage=calculated_item['percentual_ipi'],  # CORREÇÃO: Incluir IPI percentage
                commission_percentage=0,  # Será calculado pela rentabilidade
                # CORREÇÃO: Incluir weight_difference_display
                weight_difference_display=calculated_item.get('weight_difference_display')
            )
            
            # 🔍 DEBUG: Log BudgetItemCreate após criação
            print(f"🔍 DEBUG - BudgetItemCreate {i}: delivery_time = {repr(budget_item.delivery_time)}")
            
            items_for_creation.append(budget_item)
        
        # Criar orçamento completo para salvar
        complete_budget_data = BudgetCreate(
            order_number=order_number,
            client_name=budget_data.client_name,
            notes=budget_data.notes,
            expires_at=budget_data.expires_at,
            # CORREÇÃO: Incluir campos prazo_medio, outras_despesas_totais e freight_type
            prazo_medio=budget_data.prazo_medio,
            outras_despesas_totais=budget_data.outras_despesas_totais,
            freight_type=budget_data.freight_type,
            freight_value_total=budget_data.freight_value_total,  # CORREÇÃO: Incluir freight_value_total
            payment_condition=budget_data.payment_condition,
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


# Removido: endpoint de cálculo automático de markup


# Removido: endpoint de sugestão de preço via markup





@router.get("/{budget_id}/export-pdf")
async def export_budget_as_pdf(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
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
        
        # Gerar PDF usando template oficial com token de autenticação
        pdf_content = await pdf_export_service.generate_proposal_pdf(budget, credentials.credentials)
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
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
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
        
        # Gerar PDF usando template oficial com token de autenticação
        pdf_content = await pdf_export_service.generate_proposal_pdf(budget, credentials.credentials)
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

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Integer, and_, text
from app.core.database import get_db
from app.core.security import get_current_active_user, CurrentUser
from app.models.budget import Budget, BudgetStatus

router = APIRouter()


# Configurar logging
logger = logging.getLogger(__name__)


@router.get("/stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    start_date: str = Query(..., description="Data inicial (YYYY-MM-DD)"),
    end_date: str = Query(..., description="Data final (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Obter estatísticas do dashboard"""
    try:
        # Converter strings para datetime
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        logger.debug(f"Dashboard stats period: {start_date} to {end_date}")
        
        # Contar orçamentos por status
        status_counts = {}
        for budget_status in BudgetStatus:
            try:
                result = await db.execute(
                    select(func.count(Budget.id))
                    .where(
                        and_(
                            Budget.created_at >= start_dt,
                            Budget.created_at < end_dt,
                            Budget.status == budget_status
                        )
                    )
                )
                count = result.scalar() or 0
                status_counts[budget_status.value] = count
                
            except Exception as status_error:
                logger.error(f"Error fetching status {budget_status.value}: {status_error}")
                
                # Tentar com cast para Integer
                try:
                    result = await db.execute(
                        select(func.count(Budget.id))
                        .where(
                            and_(
                                Budget.created_at >= start_dt,
                                Budget.created_at < end_dt,
                                cast(Budget.status, Integer) == budget_status.value
                            )
                        )
                    )
                    count = result.scalar() or 0
                    status_counts[budget_status.value] = count
                    
                except Exception as cast_error:
                    logger.error(f"Error even with cast: {cast_error}")
                    status_counts[budget_status.value] = 0
            
            logger.debug(f"Status {budget_status.value}: {count}")
        
        # Total de orçamentos do período
        total_query = """
            SELECT COUNT(*) 
            FROM budgets 
            WHERE created_at >= :start_date 
            AND created_at <= :end_date
        """
        total_params = {"start_date": start_dt, "end_date": end_dt}
        
        result = await db.execute(text(total_query), total_params)
        total_budgets = result.scalar() or 0
        print(f"DEBUG - Total orçamentos: {total_budgets}")
        
        # Valor total dos orçamentos do período
        value_query = """
            SELECT COALESCE(SUM(total_sale_value), 0) 
            FROM budgets 
            WHERE created_at >= :start_date 
            AND created_at <= :end_date
        """
        value_params = {"start_date": start_dt, "end_date": end_dt}
        
        result = await db.execute(text(value_query), value_params)
        total_value = result.scalar() or 0
        print(f"DEBUG - Valor total: {total_value}")
        
        # Orçamentos aprovados do período
        approved_query = """
            SELECT COUNT(*), COALESCE(SUM(total_sale_value), 0)
            FROM budgets 
            WHERE status = 'approved' 
            AND created_at >= :start_date 
            AND created_at <= :end_date
        """
        approved_params = {"start_date": start_dt, "end_date": end_dt}
        
        result = await db.execute(text(approved_query), approved_params)
        approved_result = result.first()
        approved_count = approved_result[0] if approved_result else 0
        approved_value = approved_result[1] if approved_result else 0
        print(f"DEBUG - Aprovados: {approved_count}, Valor aprovado: {approved_value}")
        
        # Se não há orçamentos no período, vamos verificar se existem orçamentos de outros períodos
        if total_budgets == 0:
            check_query = "SELECT COUNT(*), MIN(created_at), MAX(created_at) FROM budgets"
            check_params = {}
            
            result = await db.execute(text(check_query), check_params)
            total_check = result.first()
            print(f"DEBUG - Verificação geral: {total_check[0]} orçamentos, de {total_check[1]} até {total_check[2]}")
        
        # Buscar orçamentos recentes
        recent_query = """
            SELECT id, client_name, total_sale_value, status, created_at
            FROM budgets 
            WHERE created_at >= :start_date 
            AND created_at <= :end_date
            ORDER BY created_at DESC
            LIMIT 10
        """
        recent_params = {"start_date": start_dt, "end_date": end_dt}
        
        result = await db.execute(text(recent_query), recent_params)
        recent_budgets_data = []
        for row in result.fetchall():
            recent_budgets_data.append({
                "id": row[0],
                "client_name": row[1],
                "total_sale_value": float(row[2] or 0),
                "status": row[3],
                "created_at": row[4].isoformat() if row[4] else None
            })
        
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "totals": {
                "total_budgets": total_budgets,
                "total_value": float(total_value or 0),
                "approved_count": approved_count,
                "approved_value": float(approved_value or 0)
            },
            "status_counts": status_counts,
            "recent_budgets": recent_budgets_data
        }
        
    except Exception as e:
        logger.error(f"Error generating dashboard stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

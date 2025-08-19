from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_active_user, CurrentUser
from app.models.budget import BudgetStatus

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    days: int = Query(30, description="Filtro de dias (1=hoje, 3, 7, 15, 30)"),
    custom_start: Optional[str] = Query(None, description="Data inicial customizada (YYYY-MM-DD)"),
    custom_end: Optional[str] = Query(None, description="Data final customizada (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_active_user)
):
    """Estatísticas do dashboard para administradores"""
    
    # Apenas administradores podem ver todas as estatísticas
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem acessar estas estatísticas."
        )
    
    try:
        # Calcular período
        end_date = datetime.now()
        
        if custom_start and custom_end:
            # Período customizado
            start_date = datetime.strptime(custom_start, "%Y-%m-%d")
            end_date = datetime.strptime(custom_end, "%Y-%m-%d")
            # Ajustar o end_date para incluir o dia completo
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            # Período baseado em dias
            if days == 1:
                # Para "hoje", começar desde 00:00:00
                start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                start_date = end_date - timedelta(days=days)
        
        print(f"DEBUG - Período: {start_date} até {end_date}")
        
        # Buscar estatísticas por status - com tratamento de erro para enum
        status_counts = {}
        for budget_status in BudgetStatus:
            try:
                result = await db.execute(
                    text("""
                        SELECT COUNT(*) 
                        FROM budgets 
                        WHERE status = :status 
                        AND created_at >= :start_date 
                        AND created_at <= :end_date
                    """),
                    {"status": budget_status.value, "start_date": start_date, "end_date": end_date}
                )
                count = result.scalar() or 0
            except Exception as status_error:
                print(f"DEBUG - Erro ao buscar status {budget_status.value}: {status_error}")
                # Se der erro com enum, vamos buscar usando CAST para tratar o problema
                try:
                    result = await db.execute(
                        text("""
                            SELECT COUNT(*) 
                            FROM budgets 
                            WHERE status::text = :status 
                            AND created_at >= :start_date 
                            AND created_at <= :end_date
                        """),
                        {"status": budget_status.value, "start_date": start_date, "end_date": end_date}
                    )
                    count = result.scalar() or 0
                except Exception as cast_error:
                    print(f"DEBUG - Erro mesmo com cast: {cast_error}")
                    count = 0
            
            status_counts[budget_status.value] = count
            print(f"DEBUG - Status {budget_status.value}: {count}")
        
        # Total de orçamentos do período
        result = await db.execute(
            text("""
                SELECT COUNT(*) 
                FROM budgets 
                WHERE created_at >= :start_date 
                AND created_at <= :end_date
            """),
            {"start_date": start_date, "end_date": end_date}
        )
        total_budgets = result.scalar() or 0
        print(f"DEBUG - Total orçamentos: {total_budgets}")
        
        # Valor total dos orçamentos do período
        result = await db.execute(
            text("""
                SELECT COALESCE(SUM(total_sale_value), 0) 
                FROM budgets 
                WHERE created_at >= :start_date 
                AND created_at <= :end_date
            """),
            {"start_date": start_date, "end_date": end_date}
        )
        total_value = result.scalar() or 0
        print(f"DEBUG - Valor total: {total_value}")
        
        # Orçamentos aprovados do período
        result = await db.execute(
            text("""
                SELECT COUNT(*), COALESCE(SUM(total_sale_value), 0)
                FROM budgets 
                WHERE status = 'approved' 
                AND created_at >= :start_date 
                AND created_at <= :end_date
            """),
            {"start_date": start_date, "end_date": end_date}
        )
        approved_result = result.first()
        approved_count = approved_result[0] if approved_result else 0
        approved_value = approved_result[1] if approved_result else 0
        print(f"DEBUG - Aprovados: {approved_count}, Valor aprovado: {approved_value}")
        
        # Se não há orçamentos no período, vamos verificar se existem orçamentos de outros períodos
        if total_budgets == 0:
            result = await db.execute(text("SELECT COUNT(*), MIN(created_at), MAX(created_at) FROM budgets"))
            total_check = result.first()
            print(f"DEBUG - Verificação geral: {total_check[0]} orçamentos, de {total_check[1]} até {total_check[2]}")
        
        return {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": days if not (custom_start and custom_end) else None
            },
            "budgets_by_status": status_counts,
            "total_budgets": total_budgets,
            "total_value": float(total_value),
            "approved_budgets": approved_count,
            "approved_value": float(approved_value),
            "conversion_rate": (approved_count / total_budgets * 100) if total_budgets > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}"
        )

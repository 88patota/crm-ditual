import pytest

from app.models.budget import BudgetStatus
from app.schemas.budget import BudgetCreate, BudgetItemSimplified, BudgetSimplifiedCreate
from app.services.budget_service import BudgetService


@pytest.mark.parametrize(
    "status",
    [
        BudgetStatus.DRAFT,
        BudgetStatus.PENDING,
        BudgetStatus.APPROVED,
        BudgetStatus.LOST,
        BudgetStatus.SENT,
    ],
)
def test_resolve_budget_status_accepts_all_known_statuses(status: BudgetStatus):
    assert BudgetService._resolve_budget_status(status) == status.value
    assert BudgetService._resolve_budget_status(status.value) == status.value


@pytest.mark.parametrize(
    "status",
    [
        BudgetStatus.PENDING,
        BudgetStatus.APPROVED,
        BudgetStatus.LOST,
        BudgetStatus.SENT,
    ],
)
def test_budget_create_accepts_non_draft_status(status: BudgetStatus):
    budget = BudgetCreate(
        order_number="PED-001",
        client_name="Cliente",
        status=status,
        items=[],
    )
    assert budget.status == status


@pytest.mark.parametrize(
    "status",
    [
        BudgetStatus.PENDING,
        BudgetStatus.APPROVED,
        BudgetStatus.LOST,
        BudgetStatus.SENT,
    ],
)
def test_budget_simplified_create_accepts_non_draft_status(status: BudgetStatus):
    simplified = BudgetSimplifiedCreate(
        client_name="Cliente",
        status=status,
        items=[
            BudgetItemSimplified(
                description="Item",
                peso_compra=1.0,
                valor_com_icms_compra=100.0,
                percentual_icms_compra=0.18,
                outras_despesas_item=0.0,
                valor_com_icms_venda=150.0,
                percentual_icms_venda=0.18,
                percentual_ipi=0.0,
            )
        ],
    )
    assert simplified.status == status


def test_resolve_budget_status_rejects_invalid_value():
    with pytest.raises(ValueError):
        BudgetService._resolve_budget_status("invalido")

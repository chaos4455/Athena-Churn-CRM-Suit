from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.infrastructure.repositories.sqlite_client_repository import SQLiteClientRepository
from app.infrastructure.repositories.sqlite_action_repository import SQLiteActionRepository
from app.domain.services.dashboard_service import DashboardService
from app.application.use_cases.dashboard.get_dashboard_indicators import GetDashboardIndicatorsUseCase
from app.api.v1.schemas.dashboard_schema import DashboardIndicators

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/indicators", response_model=DashboardIndicators)
def get_indicators(
    branch:    Optional[str] = Query(None, description="Filtrar por filial"),
    state:     Optional[str] = Query(None, description="Filtrar por estado (UF)"),
    seller_id: Optional[str] = Query(None, description="Filtrar por vendedor (UUID)"),
    db: Session = Depends(get_db),
):
    card_repo   = SQLiteCardRepository(db)
    client_repo = SQLiteClientRepository(db)
    action_repo = SQLiteActionRepository(db)
    service     = DashboardService(card_repo, client_repo, action_repo)
    return GetDashboardIndicatorsUseCase(service).execute(
        branch=branch, state=state, seller_id=seller_id
    )


@router.get("/filters")
def get_filter_options(db: Session = Depends(get_db)):
    """Retorna listas de filiais e estados disponíveis para os filtros."""
    card_repo = SQLiteCardRepository(db)
    return {
        "branches": card_repo.list_branches(),
        "states":   card_repo.list_states(),
    }

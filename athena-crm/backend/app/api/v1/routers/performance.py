from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.infrastructure.repositories.sqlite_action_repository import SQLiteActionRepository
from app.infrastructure.repositories.sqlite_seller_repository import SQLiteSellerRepository
from app.domain.services.performance_service import PerformanceService
from app.application.use_cases.dashboard.get_performance_metrics import GetPerformanceMetricsUseCase
from app.api.v1.schemas.dashboard_schema import PerformanceMetrics, TeamPerformance, SellerPerformanceRow

router = APIRouter(prefix="/performance", tags=["Performance"])


@router.get("/team", response_model=TeamPerformance)
def get_team_performance(
    branch:    Optional[str] = Query(None),
    state:     Optional[str] = Query(None),
    cycle_id:  Optional[str] = Query(None),
    archived:  bool          = Query(False),
    db: Session = Depends(get_db),
):
    """Visão gerencial — performance de todos os vendedores."""
    card_repo   = SQLiteCardRepository(db)
    action_repo = SQLiteActionRepository(db)
    seller_repo = SQLiteSellerRepository(db)
    service     = PerformanceService(card_repo, action_repo)

    sellers = seller_repo.find_all()
    rows: List[SellerPerformanceRow] = []
    totals = {"total_cards":0,"converted":0,"declined":0,"in_progress":0,
              "in_negotiation":0,"backlog":0,"total_actions":0}

    for s in sellers:
        m = service.get_seller_performance(s.id, branch=branch, state=state, archived=archived)
        rows.append(SellerPerformanceRow(
            seller_id=s.id, seller_name=s.name,
            branch=s.branch, state=s.state,
            **{k: v for k, v in m.items() if k != "seller_id"},
        ))
        for k in totals:
            totals[k] += m.get(k, 0)

    total_cards = totals["total_cards"]
    converted   = totals["converted"]
    totals_obj  = PerformanceMetrics(
        seller_id="__team__",
        conversion_rate=round(converted/total_cards*100, 2) if total_cards else 0.0,
        **totals,
    )
    return TeamPerformance(sellers=rows, totals=totals_obj)


@router.get("/{seller_id}", response_model=PerformanceMetrics)
def get_seller_performance(
    seller_id: str,
    branch:    Optional[str] = Query(None),
    state:     Optional[str] = Query(None),
    archived:  bool          = Query(False),
    db: Session = Depends(get_db),
):
    card_repo   = SQLiteCardRepository(db)
    action_repo = SQLiteActionRepository(db)
    service     = PerformanceService(card_repo, action_repo)
    return GetPerformanceMetricsUseCase(service).execute(
        seller_id, branch=branch, state=state, archived=archived
    )

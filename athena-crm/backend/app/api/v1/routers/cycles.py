"""
POST /cycles/close
Fecha o ciclo atual:
  1. Arquiva todos os cards ativos (is_archived = True)
  2. Reseta os indicadores de risco dos clientes (churn_risk_score = 0, is_at_risk = False)
Históricos, ações e métricas são preservados.
Requer a senha de fechamento definida em config.yaml / settings.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import CardModel, ClientModel
from app.core.config import settings

router = APIRouter(prefix="/cycles", tags=["Cycles"])


class CycleCloseRequest(BaseModel):
    password: str
    cycle_id: Optional[str] = None   # e.g. "2025-04" — defaults to current month


class CycleCloseResponse(BaseModel):
    archived:        int
    clients_reset:   int
    cycle_id:        str
    closed_at:       str
    message:         str


@router.post("/close", response_model=CycleCloseResponse)
def close_cycle(body: CycleCloseRequest, db: Session = Depends(get_db)):
    # ── Auth ──────────────────────────────────────────────────
    if body.password != settings.CYCLE_CLOSE_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta. Verifique config.yaml → security.cycle_close_password",
        )

    now      = datetime.utcnow()
    cycle_id = body.cycle_id or now.strftime("%Y-%m")

    # ── 1. Archive all active cards ───────────────────────────
    cards_archived = (
        db.query(CardModel)
        .filter(CardModel.is_archived == False)  # noqa: E712
        .update(
            {
                "is_archived": True,
                "archived_at": now,
                "cycle_id":    cycle_id,
                "updated_at":  now,
            },
            synchronize_session="fetch",
        )
    )

    # ── 2. Reset client risk indicators ───────────────────────
    # Clears churn scores and at-risk flags so the new cycle starts clean.
    # LTV and avg_ticket are preserved (historical financial data).
    clients_reset = (
        db.query(ClientModel)
        .filter(ClientModel.is_at_risk == True)  # noqa: E712
        .update(
            {
                "churn_risk_score": 0.0,
                "is_at_risk":       False,
                "updated_at":       now,
            },
            synchronize_session="fetch",
        )
    )

    db.commit()

    return CycleCloseResponse(
        archived=cards_archived,
        clients_reset=clients_reset,
        cycle_id=cycle_id,
        closed_at=now.isoformat(),
        message=(
            f"Ciclo {cycle_id} fechado. "
            f"{cards_archived} card(s) arquivado(s), "
            f"{clients_reset} cliente(s) resetado(s)."
        ),
    )

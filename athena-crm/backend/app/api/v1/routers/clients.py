from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_client_repository import SQLiteClientRepository
from app.infrastructure.repositories.sqlite_history_repository import SQLiteHistoryRepository
from app.application.use_cases.clients.list_clients import ListClientsUseCase
from app.application.use_cases.clients.get_client import GetClientUseCase
from app.application.use_cases.clients.search_clients import SearchClientsUseCase
from app.application.use_cases.clients.get_client_history import GetClientHistoryUseCase
from app.api.v1.schemas.client_schema import ClientResponse
from app.core.exceptions import EntityNotFoundException, not_found

router = APIRouter(prefix="/clients", tags=["Clients"])


def _client_repo(db: Session = Depends(get_db)):
    return SQLiteClientRepository(db)


def _history_repo(db: Session = Depends(get_db)):
    return SQLiteHistoryRepository(db)


@router.get("/", response_model=List[ClientResponse])
def list_clients(
    skip:   int            = 0,
    limit:  int            = 100,
    search: Optional[str]  = Query(None),
    branch: Optional[str]  = Query(None),
    state:  Optional[str]  = Query(None),
    repo=Depends(_client_repo),
):
    if search:
        clients = SearchClientsUseCase(repo).execute(search)
    else:
        clients = ListClientsUseCase(repo).execute(skip=skip, limit=limit)

    # Filtros opcionais
    if branch:
        clients = [c for c in clients if c.branch == branch]
    if state:
        clients = [c for c in clients if c.state == state]

    return [c.__dict__ for c in clients]


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: str, repo=Depends(_client_repo)):
    try:
        return GetClientUseCase(repo).execute(client_id).__dict__
    except EntityNotFoundException:
        raise not_found("Client", client_id)


@router.get("/{client_id}/history")
def get_client_history(
    client_id: str,
    cycle_id:  Optional[str] = Query(None, description="Filtrar por ciclo"),
    client_repo=Depends(_client_repo),
    history_repo=Depends(_history_repo),
    db: Session = Depends(get_db),
):
    from app.infrastructure.database.models import CardModel, SellerModel

    try:
        if not client_repo.find_by_id(client_id):
            raise not_found("Client", client_id)
        histories = history_repo.find_by_client(client_id, cycle_id=cycle_id)

        result = []
        for h in histories:
            d = h.__dict__.copy()

            # Enrich with seller name
            seller = db.query(SellerModel).filter_by(id=h.seller_id).first()
            d["seller_name"] = seller.name if seller else None

            # Enrich with card info (current state)
            if h.card_id and h.card_id != "00000000-0000-0000-0000-000000000000":
                card = db.query(CardModel).filter_by(id=h.card_id).first()
                if card:
                    d["card_title"]       = card.title
                    d["card_stage_now"]   = card.stage.value if hasattr(card.stage, "value") else str(card.stage)
                    d["card_cycle_id"]    = card.cycle_id
                    d["card_is_archived"] = card.is_archived
                    d["card_archived_at"] = card.archived_at.isoformat() if card.archived_at else None
                else:
                    d["card_title"] = d["card_stage_now"] = d["card_cycle_id"] = None
                    d["card_is_archived"] = None
                    d["card_archived_at"] = None
            else:
                d["card_title"] = d["card_stage_now"] = d["card_cycle_id"] = None
                d["card_is_archived"] = None
                d["card_archived_at"] = None

            result.append(d)

        return result
    except EntityNotFoundException:
        raise not_found("Client", client_id)

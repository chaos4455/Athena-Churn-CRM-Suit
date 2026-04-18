from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_action_repository import SQLiteActionRepository
from app.infrastructure.repositories.sqlite_history_repository import SQLiteHistoryRepository
from app.infrastructure.database.models import ActionModel, CardModel, ClientModel, SellerModel
from app.application.use_cases.actions.register_action import RegisterActionUseCase
from app.application.use_cases.actions.list_actions import ListActionsUseCase
from app.application.use_cases.actions.update_action import UpdateActionUseCase
from app.application.dtos.action_dto import CreateActionDTO, UpdateActionDTO
from app.api.v1.schemas.action_schema import ActionCreate, ActionUpdate, ActionResponse
from app.core.exceptions import EntityNotFoundException, not_found

router = APIRouter(prefix="/actions", tags=["Actions"])


def _action_repo(db: Session = Depends(get_db)):
    return SQLiteActionRepository(db)


def _history_repo(db: Session = Depends(get_db)):
    return SQLiteHistoryRepository(db)


def _enrich(action_dict: dict, db: Session) -> dict:
    """Enrich action with names + current card state (the 'resultado')."""
    card   = db.query(CardModel).filter_by(id=action_dict.get("card_id")).first()
    client = db.query(ClientModel).filter_by(id=action_dict.get("client_id")).first()
    seller = db.query(SellerModel).filter_by(id=action_dict.get("seller_id")).first()

    action_dict["client_name"] = client.name if client else None
    action_dict["seller_name"] = seller.name if seller else None

    if card:
        action_dict["card_title"]       = card.title
        action_dict["card_stage"]       = card.stage.value if hasattr(card.stage, "value") else str(card.stage)
        action_dict["card_cycle_id"]    = card.cycle_id
        action_dict["card_is_archived"] = card.is_archived
        action_dict["card_archived_at"] = card.archived_at
    else:
        action_dict["card_title"]       = None
        action_dict["card_stage"]       = None
        action_dict["card_cycle_id"]    = None
        action_dict["card_is_archived"] = None
        action_dict["card_archived_at"] = None

    return action_dict


@router.get("/", response_model=List[ActionResponse])
def list_actions(
    card_id:   Optional[str] = Query(None),
    seller_id: Optional[str] = Query(None),
    skip:  int = 0,
    limit: int = 100,
    action_repo=Depends(_action_repo),
    db: Session = Depends(get_db),
):
    actions = ListActionsUseCase(action_repo).execute(
        card_id=card_id, seller_id=seller_id, skip=skip, limit=limit
    )
    return [_enrich(a.__dict__.copy(), db) for a in actions]


@router.post("/", response_model=ActionResponse, status_code=201)
def register_action(
    body: ActionCreate,
    action_repo=Depends(_action_repo),
    history_repo=Depends(_history_repo),
    db: Session = Depends(get_db),
):
    dto    = CreateActionDTO(**body.model_dump())
    action = RegisterActionUseCase(action_repo, history_repo).execute(dto)
    return _enrich(action.__dict__.copy(), db)


@router.patch("/{action_id}", response_model=ActionResponse)
def update_action(
    action_id: str,
    body: ActionUpdate,
    action_repo=Depends(_action_repo),
    db: Session = Depends(get_db),
):
    try:
        dto    = UpdateActionDTO(**body.model_dump(exclude_none=True))
        action = UpdateActionUseCase(action_repo).execute(action_id, dto)
        return _enrich(action.__dict__.copy(), db)
    except EntityNotFoundException:
        raise not_found("Action", action_id)


@router.delete("/{action_id}", status_code=204)
def delete_action(action_id: str, action_repo=Depends(_action_repo)):
    if not action_repo.find_by_id(action_id):
        raise not_found("Action", action_id)
    action_repo.delete(action_id)

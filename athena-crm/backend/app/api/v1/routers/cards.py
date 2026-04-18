from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.infrastructure.repositories.sqlite_client_repository import SQLiteClientRepository
from app.application.use_cases.cards.create_card import CreateCardUseCase
from app.application.use_cases.cards.update_card import UpdateCardUseCase
from app.application.use_cases.cards.delete_card import DeleteCardUseCase
from app.application.use_cases.cards.list_cards import ListCardsUseCase
from app.application.use_cases.cards.get_card import GetCardUseCase
from app.application.use_cases.cards.move_card_stage import MoveCardStageUseCase
from app.application.dtos.card_dto import CreateCardDTO, UpdateCardDTO
from app.api.v1.schemas.card_schema import CardCreate, CardUpdate, CardMoveStage, CardResponse
from app.domain.value_objects.card_stage import CardStage
from app.core.exceptions import EntityNotFoundException, not_found

router = APIRouter(prefix="/cards", tags=["Cards"])


def _card_repo(db: Session = Depends(get_db)):
    return SQLiteCardRepository(db)


def _client_repo(db: Session = Depends(get_db)):
    return SQLiteClientRepository(db)


@router.get("/", response_model=List[CardResponse])
def list_cards(
    seller_id: Optional[str]    = Query(None),
    stage:     Optional[CardStage] = Query(None),
    branch:    Optional[str]    = Query(None),
    state:     Optional[str]    = Query(None),
    cycle_id:  Optional[str]    = Query(None),
    archived:  bool             = Query(False),
    skip:      int              = 0,
    limit:     int              = 200,
    card_repo=Depends(_card_repo),
):
    cards = ListCardsUseCase(card_repo).execute(
        seller_id=seller_id, stage=stage,
        branch=branch, state=state,
        cycle_id=cycle_id, archived=archived,
        skip=skip, limit=limit,
    )
    return [c.__dict__ for c in cards]


@router.post("/", response_model=CardResponse, status_code=201)
def create_card(
    body: CardCreate,
    card_repo=Depends(_card_repo),
    client_repo=Depends(_client_repo),
):
    try:
        dto = CreateCardDTO(**body.model_dump())
        card = CreateCardUseCase(card_repo, client_repo).execute(dto)
        return card.__dict__
    except EntityNotFoundException:
        raise not_found("Client", body.client_id)


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: str, card_repo=Depends(_card_repo)):
    try:
        return GetCardUseCase(card_repo).execute(card_id).__dict__
    except EntityNotFoundException:
        raise not_found("Card", card_id)


@router.patch("/{card_id}", response_model=CardResponse)
def update_card(card_id: str, body: CardUpdate, card_repo=Depends(_card_repo)):
    try:
        dto = UpdateCardDTO(**body.model_dump(exclude_none=True))
        return UpdateCardUseCase(card_repo).execute(card_id, dto).__dict__
    except EntityNotFoundException:
        raise not_found("Card", card_id)


@router.patch("/{card_id}/stage", response_model=CardResponse)
def move_stage(card_id: str, body: CardMoveStage, card_repo=Depends(_card_repo)):
    try:
        return MoveCardStageUseCase(card_repo).execute(card_id, body.stage).__dict__
    except EntityNotFoundException:
        raise not_found("Card", card_id)


@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: str, card_repo=Depends(_card_repo)):
    try:
        DeleteCardUseCase(card_repo).execute(card_id)
    except EntityNotFoundException:
        raise not_found("Card", card_id)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_client_repository import SQLiteClientRepository
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.infrastructure.repositories.sqlite_history_repository import SQLiteHistoryRepository
from app.application.use_cases.etl.ingest_clients import IngestClientsUseCase
from app.application.use_cases.etl.ingest_cards import IngestCardsUseCase
from app.application.dtos.etl_dto import ETLClientRecord, ETLCardRecord
from app.api.v1.schemas.etl_schema import ETLClientIn, ETLCardIn, ETLIngestResponse

router = APIRouter(prefix="/etl", tags=["ETL"])


@router.post("/clients", response_model=ETLIngestResponse)
def ingest_clients(payload: List[ETLClientIn], db: Session = Depends(get_db)):
    repo    = SQLiteClientRepository(db)
    records = [ETLClientRecord(**item.model_dump()) for item in payload]
    result  = IngestClientsUseCase(repo).execute(records)
    return {"created": result.created, "updated": result.updated,
            "archived": result.archived, "errors": result.errors}


@router.post("/cards", response_model=ETLIngestResponse)
def ingest_cards(payload: List[ETLCardIn], db: Session = Depends(get_db)):
    card_repo    = SQLiteCardRepository(db)
    client_repo  = SQLiteClientRepository(db)
    history_repo = SQLiteHistoryRepository(db)
    records      = [ETLCardRecord(**item.model_dump()) for item in payload]
    result       = IngestCardsUseCase(card_repo, client_repo, history_repo).execute(records)
    return {"created": result.created, "updated": result.updated,
            "archived": result.archived, "errors": result.errors}

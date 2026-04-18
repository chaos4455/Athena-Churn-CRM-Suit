from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.history import History
from app.domain.repositories.history_repository import HistoryRepository
from app.infrastructure.database.models import HistoryModel


def _to_entity(m: HistoryModel) -> History:
    return History(
        id=m.id, client_id=m.client_id, card_id=m.card_id,
        seller_id=m.seller_id, content=m.content,
        history_type=m.history_type or "note",
        card_stage=m.card_stage,
        cycle_id=m.cycle_id,
        created_at=m.created_at,
    )


class SQLiteHistoryRepository(HistoryRepository):

    def __init__(self, db: Session):
        self._db = db

    def save(self, history: History) -> History:
        model = HistoryModel(**{k: v for k, v in history.__dict__.items() if not k.startswith("_")})
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def find_by_client(self, client_id: str, cycle_id: Optional[str] = None) -> List[History]:
        q = (self._db.query(HistoryModel)
             .filter_by(client_id=client_id)
             .order_by(HistoryModel.created_at.desc()))
        if cycle_id:
            q = q.filter(HistoryModel.cycle_id == cycle_id)
        return [_to_entity(r) for r in q.all()]

    def find_by_card(self, card_id: str) -> List[History]:
        rows = (self._db.query(HistoryModel)
                .filter_by(card_id=card_id)
                .order_by(HistoryModel.created_at.desc())
                .all())
        return [_to_entity(r) for r in rows]

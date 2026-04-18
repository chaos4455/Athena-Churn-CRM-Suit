from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository
from app.infrastructure.database.models import ActionModel


def _to_entity(m: ActionModel) -> Action:
    return Action(
        id=m.id, card_id=m.card_id, client_id=m.client_id,
        seller_id=m.seller_id, action_type=m.action_type,
        description=m.description, outcome=m.outcome,
        status=m.status, scheduled_at=m.scheduled_at,
        completed_at=m.completed_at,
        created_at=m.created_at, updated_at=m.updated_at,
    )


class SQLiteActionRepository(ActionRepository):

    def __init__(self, db: Session):
        self._db = db

    def save(self, action: Action) -> Action:
        existing = self._db.query(ActionModel).filter_by(id=action.id).first()
        if existing:
            for k, v in action.__dict__.items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            self._db.commit()
            self._db.refresh(existing)
            return _to_entity(existing)
        model = ActionModel(**{k: v for k, v in action.__dict__.items() if not k.startswith("_")})
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def find_by_id(self, id: str) -> Optional[Action]:
        m = self._db.query(ActionModel).filter_by(id=id).first()
        return _to_entity(m) if m else None

    def find_by_card(self, card_id: str) -> List[Action]:
        rows = self._db.query(ActionModel).filter_by(card_id=card_id).all()
        return [_to_entity(r) for r in rows]

    def find_by_client(self, client_id: str) -> List[Action]:
        rows = self._db.query(ActionModel).filter_by(client_id=client_id).all()
        return [_to_entity(r) for r in rows]

    def find_by_seller(self, seller_id: str) -> List[Action]:
        rows = self._db.query(ActionModel).filter_by(seller_id=seller_id).all()
        return [_to_entity(r) for r in rows]

    def find_all(self, skip: int = 0, limit: int = 100) -> List[Action]:
        rows = self._db.query(ActionModel).offset(skip).limit(limit).all()
        return [_to_entity(r) for r in rows]

    def delete(self, id: str) -> bool:
        m = self._db.query(ActionModel).filter_by(id=id).first()
        if not m:
            return False
        self._db.delete(m)
        self._db.commit()
        return True

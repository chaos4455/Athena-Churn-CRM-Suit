import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository
from app.infrastructure.database.models import ClientModel


def _to_entity(m: ClientModel) -> Client:
    return Client(
        id=m.id, name=m.name, external_id=m.external_id,
        ltv=m.ltv, avg_ticket=m.avg_ticket,
        last_purchase_date=m.last_purchase_date,
        churn_risk_score=m.churn_risk_score,
        is_at_risk=m.is_at_risk, seller_id=m.seller_id,
        created_at=m.created_at, updated_at=m.updated_at,
    )


class SQLiteClientRepository(ClientRepository):

    def __init__(self, db: Session):
        self._db = db

    def save(self, client: Client) -> Client:
        existing = self._db.query(ClientModel).filter_by(id=client.id).first()
        if existing:
            for k, v in client.__dict__.items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            self._db.commit()
            self._db.refresh(existing)
            return _to_entity(existing)
        model = ClientModel(**{k: v for k, v in client.__dict__.items() if not k.startswith("_")})
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def find_by_id(self, id: str) -> Optional[Client]:
        m = self._db.query(ClientModel).filter_by(id=id).first()
        return _to_entity(m) if m else None

    def find_by_external_id(self, external_id: str) -> Optional[Client]:
        m = self._db.query(ClientModel).filter_by(external_id=external_id).first()
        return _to_entity(m) if m else None

    def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        rows = self._db.query(ClientModel).offset(skip).limit(limit).all()
        return [_to_entity(r) for r in rows]

    def search(self, query: str) -> List[Client]:
        rows = self._db.query(ClientModel).filter(
            or_(
                ClientModel.name.ilike(f"%{query}%"),
                ClientModel.external_id.ilike(f"%{query}%"),
            )
        ).all()
        return [_to_entity(r) for r in rows]

    def find_at_risk(self) -> List[Client]:
        rows = self._db.query(ClientModel).filter_by(is_at_risk=True).all()
        return [_to_entity(r) for r in rows]

    def delete(self, id: str) -> bool:
        m = self._db.query(ClientModel).filter_by(id=id).first()
        if not m:
            return False
        self._db.delete(m)
        self._db.commit()
        return True

    def count(self) -> int:
        return self._db.query(ClientModel).count()

    def count_at_risk(self) -> int:
        return self._db.query(ClientModel).filter_by(is_at_risk=True).count()

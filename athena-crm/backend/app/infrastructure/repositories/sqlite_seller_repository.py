from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.seller import Seller
from app.domain.repositories.seller_repository import SellerRepository
from app.infrastructure.database.models import SellerModel


def _to_entity(m: SellerModel) -> Seller:
    return Seller(
        id=m.id, name=m.name, email=m.email,
        role=m.role, branch=m.branch, state=m.state,
        is_active=m.is_active, created_at=m.created_at,
    )


class SQLiteSellerRepository(SellerRepository):

    def __init__(self, db: Session):
        self._db = db

    def save(self, seller: Seller) -> Seller:
        existing = self._db.query(SellerModel).filter_by(id=seller.id).first()
        if existing:
            for k, v in seller.__dict__.items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            self._db.commit()
            self._db.refresh(existing)
            return _to_entity(existing)
        model = SellerModel(**{k: v for k, v in seller.__dict__.items() if not k.startswith("_")})
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def find_by_id(self, id: str) -> Optional[Seller]:
        m = self._db.query(SellerModel).filter_by(id=id).first()
        return _to_entity(m) if m else None

    def find_all(self) -> List[Seller]:
        rows = self._db.query(SellerModel).all()
        return [_to_entity(r) for r in rows]

    def find_by_email(self, email: str) -> Optional[Seller]:
        m = self._db.query(SellerModel).filter_by(email=email).first()
        return _to_entity(m) if m else None

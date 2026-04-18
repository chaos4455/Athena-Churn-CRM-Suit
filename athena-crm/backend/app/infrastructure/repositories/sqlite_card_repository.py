from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.value_objects.card_stage import CardStage
from app.infrastructure.database.models import CardModel


def _to_entity(m: CardModel) -> Card:
    return Card(
        id=m.id, client_id=m.client_id, client_name=m.client_name,
        seller_id=m.seller_id, seller_name=m.seller_name or "",
        stage=m.stage, title=m.title, description=m.description,
        ltv=m.ltv, avg_ticket=m.avg_ticket,
        last_purchase_date=m.last_purchase_date,
        value_at_risk=m.value_at_risk,
        branch=m.branch, state=m.state,
        cycle_id=m.cycle_id,
        is_archived=m.is_archived, archived_at=m.archived_at,
        created_at=m.created_at, updated_at=m.updated_at,
    )


class SQLiteCardRepository(CardRepository):

    def __init__(self, db: Session):
        self._db = db

    def save(self, card: Card) -> Card:
        existing = self._db.query(CardModel).filter_by(id=card.id).first()
        if existing:
            for k, v in card.__dict__.items():
                if not k.startswith("_"):
                    setattr(existing, k, v)
            self._db.commit()
            self._db.refresh(existing)
            return _to_entity(existing)
        model = CardModel(**{k: v for k, v in card.__dict__.items() if not k.startswith("_")})
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def find_by_id(self, id: str) -> Optional[Card]:
        m = self._db.query(CardModel).filter_by(id=id).first()
        return _to_entity(m) if m else None

    def find_all(self, skip: int = 0, limit: int = 200, archived: bool = False) -> List[Card]:
        rows = (self._db.query(CardModel)
                .filter_by(is_archived=archived)
                .offset(skip).limit(limit).all())
        return [_to_entity(r) for r in rows]

    def find_by_seller(self, seller_id: str, archived: bool = False) -> List[Card]:
        rows = (self._db.query(CardModel)
                .filter_by(seller_id=seller_id, is_archived=archived).all())
        return [_to_entity(r) for r in rows]

    def find_by_stage(self, stage: CardStage, archived: bool = False) -> List[Card]:
        rows = (self._db.query(CardModel)
                .filter_by(stage=stage, is_archived=archived).all())
        return [_to_entity(r) for r in rows]

    def find_by_client(self, client_id: str) -> List[Card]:
        rows = (self._db.query(CardModel)
                .filter_by(client_id=client_id)
                .order_by(CardModel.created_at.desc()).all())
        return [_to_entity(r) for r in rows]

    def find_by_branch(self, branch: str, archived: bool = False) -> List[Card]:
        rows = (self._db.query(CardModel)
                .filter_by(branch=branch, is_archived=archived).all())
        return [_to_entity(r) for r in rows]

    def find_by_state(self, state: str, archived: bool = False) -> List[Card]:
        rows = (self._db.query(CardModel)
                .filter_by(state=state, is_archived=archived).all())
        return [_to_entity(r) for r in rows]

    def find_by_cycle(self, cycle_id: str) -> List[Card]:
        rows = self._db.query(CardModel).filter_by(cycle_id=cycle_id).all()
        return [_to_entity(r) for r in rows]

    def archive_old_cycles(self, current_cycle_id: str) -> int:
        """Arquiva todos os cards ativos que não pertencem ao ciclo atual."""
        now = datetime.utcnow()
        result = (self._db.query(CardModel)
                  .filter(CardModel.is_archived == False)
                  .filter(CardModel.cycle_id != current_cycle_id)
                  .update({"is_archived": True, "archived_at": now},
                          synchronize_session="fetch"))
        self._db.commit()
        return result

    def find_archived_in_cycle_transition(self, current_cycle_id: str) -> List[Card]:
        """Retorna cards recém-arquivados (ciclos anteriores ao atual)."""
        rows = (self._db.query(CardModel)
                .filter(CardModel.is_archived == True)
                .filter(CardModel.cycle_id != current_cycle_id)
                .filter(CardModel.archived_at != None)
                .all())
        return [_to_entity(r) for r in rows]

    def delete(self, id: str) -> bool:
        m = self._db.query(CardModel).filter_by(id=id).first()
        if not m:
            return False
        self._db.delete(m)
        self._db.commit()
        return True

    def count_by_stage(self, branch: Optional[str] = None,
                       state: Optional[str] = None,
                       seller_id: Optional[str] = None,
                       archived: bool = False) -> dict:
        q = (self._db.query(CardModel.stage, func.count(CardModel.id))
             .filter_by(is_archived=archived))
        if branch:
            q = q.filter(CardModel.branch == branch)
        if state:
            q = q.filter(CardModel.state == state)
        if seller_id:
            q = q.filter(CardModel.seller_id == seller_id)
        rows = q.group_by(CardModel.stage).all()
        return {stage: count for stage, count in rows}

    def total_value_at_risk(self, branch: Optional[str] = None,
                            state: Optional[str] = None,
                            seller_id: Optional[str] = None) -> float:
        q = (self._db.query(func.sum(CardModel.value_at_risk))
             .filter_by(is_archived=False))
        if branch:
            q = q.filter(CardModel.branch == branch)
        if state:
            q = q.filter(CardModel.state == state)
        if seller_id:
            q = q.filter(CardModel.seller_id == seller_id)
        return q.scalar() or 0.0

    def list_branches(self) -> List[str]:
        rows = (self._db.query(CardModel.branch)
                .filter(CardModel.branch != None)
                .distinct().all())
        return sorted([r[0] for r in rows if r[0]])

    def list_states(self) -> List[str]:
        rows = (self._db.query(CardModel.state)
                .filter(CardModel.state != None)
                .distinct().all())
        return sorted([r[0] for r in rows if r[0]])

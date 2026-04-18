"""
Athena CRM - Churn Management Suite
Popula todos os arquivos .py do backend com código real.
Rode: python populate_backend.py
"""

import os

BASE = os.path.join("athena-crm", "backend")

# ─────────────────────────────────────────────────────────────────────────────
# Conteúdo de cada arquivo
# ─────────────────────────────────────────────────────────────────────────────

FILES = {}

# ══════════════════════════════════════════════════════════════════════════════
# CORE
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/core/config.py"] = '''from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Athena CRM - Churn Management Suite"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./athena_crm.db"

    SECRET_KEY: str = "athena-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
'''

FILES["app/core/exceptions.py"] = '''from fastapi import HTTPException, status


class AthenaCRMException(Exception):
    """Base exception for Athena CRM."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundException(AthenaCRMException):
    pass


class DuplicateEntityException(AthenaCRMException):
    pass


class InvalidOperationException(AthenaCRMException):
    pass


# HTTP helpers
def not_found(entity: str, id: str | int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} with id '{id}' not found.",
    )


def bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def conflict(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
'''

FILES["app/core/logging.py"] = '''import logging
import sys


def setup_logging(debug: bool = False) -> logging.Logger:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("athena_crm")
    return logger


logger = setup_logging()
'''

FILES["app/core/__init__.py"] = '# core package\n'

# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN — Value Objects
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/domain/value_objects/churn_status.py"] = '''from enum import Enum


class ChurnStatus(str, Enum):
    DETECTED = "detected"       # Cliente detectado em risco
    IN_NEGOTIATION = "in_negotiation"
    CONVERTED = "converted"     # Churn revertido
    DECLINED = "declined"       # Perdido
    PENDING = "pending"         # Aguardando ação
'''

FILES["app/domain/value_objects/card_stage.py"] = '''from enum import Enum


class CardStage(str, Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    IN_NEGOTIATION = "in_negotiation"
    CONVERTED = "converted"
    DECLINED = "declined"
'''

FILES["app/domain/value_objects/action_type.py"] = '''from enum import Enum


class ActionType(str, Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    WHATSAPP = "whatsapp"
    NOTE = "note"
    PROPOSAL = "proposal"
'''

FILES["app/domain/value_objects/__init__.py"] = (
    "from .churn_status import ChurnStatus\n"
    "from .card_stage import CardStage\n"
    "from .action_type import ActionType\n"
    "\n__all__ = ['ChurnStatus', 'CardStage', 'ActionType']\n"
)

# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN — Entities
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/domain/entities/client.py"] = '''from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    id: str
    name: str
    external_id: str                  # ID do cliente no sistema de origem (ERP)
    ltv: float = 0.0                  # Lifetime Value
    avg_ticket: float = 0.0           # Ticket médio
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0     # 0-100
    is_at_risk: bool = False
    seller_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_at_risk(self, score: float) -> None:
        self.churn_risk_score = score
        self.is_at_risk = score >= 60.0
        self.updated_at = datetime.utcnow()
'''

FILES["app/domain/entities/card.py"] = '''from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects.card_stage import CardStage


@dataclass
class Card:
    id: str
    client_id: str
    client_name: str
    seller_id: str
    stage: CardStage = CardStage.BACKLOG
    title: str = ""
    description: str = ""
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    value_at_risk: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def move_to(self, stage: CardStage) -> None:
        self.stage = stage
        self.updated_at = datetime.utcnow()
'''

FILES["app/domain/entities/action.py"] = '''from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects.action_type import ActionType
from ..value_objects.churn_status import ChurnStatus


@dataclass
class Action:
    id: str
    card_id: str
    client_id: str
    seller_id: str
    action_type: ActionType
    description: str
    outcome: Optional[str] = None
    status: ChurnStatus = ChurnStatus.PENDING
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def complete(self, outcome: str, status: ChurnStatus) -> None:
        self.outcome = outcome
        self.status = status
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
'''

FILES["app/domain/entities/history.py"] = '''from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class History:
    id: str
    client_id: str
    card_id: Optional[str]
    seller_id: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
'''

FILES["app/domain/entities/seller.py"] = '''from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Seller:
    id: str
    name: str
    email: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
'''

FILES["app/domain/entities/__init__.py"] = (
    "from .client import Client\n"
    "from .card import Card\n"
    "from .action import Action\n"
    "from .history import History\n"
    "from .seller import Seller\n"
    "\n__all__ = ['Client', 'Card', 'Action', 'History', 'Seller']\n"
)

# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN — Repository Interfaces
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/domain/repositories/client_repository.py"] = '''from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.client import Client


class ClientRepository(ABC):

    @abstractmethod
    def save(self, client: Client) -> Client: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Client]: ...

    @abstractmethod
    def find_by_external_id(self, external_id: str) -> Optional[Client]: ...

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]: ...

    @abstractmethod
    def search(self, query: str) -> List[Client]: ...

    @abstractmethod
    def find_at_risk(self) -> List[Client]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def count_at_risk(self) -> int: ...
'''

FILES["app/domain/repositories/card_repository.py"] = '''from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.card import Card
from ..value_objects.card_stage import CardStage


class CardRepository(ABC):

    @abstractmethod
    def save(self, card: Card) -> Card: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Card]: ...

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Card]: ...

    @abstractmethod
    def find_by_seller(self, seller_id: str) -> List[Card]: ...

    @abstractmethod
    def find_by_stage(self, stage: CardStage) -> List[Card]: ...

    @abstractmethod
    def find_by_client(self, client_id: str) -> List[Card]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def count_by_stage(self) -> dict: ...

    @abstractmethod
    def total_value_at_risk(self) -> float: ...
'''

FILES["app/domain/repositories/action_repository.py"] = '''from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.action import Action


class ActionRepository(ABC):

    @abstractmethod
    def save(self, action: Action) -> Action: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Action]: ...

    @abstractmethod
    def find_by_card(self, card_id: str) -> List[Action]: ...

    @abstractmethod
    def find_by_client(self, client_id: str) -> List[Action]: ...

    @abstractmethod
    def find_by_seller(self, seller_id: str) -> List[Action]: ...

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Action]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...
'''

FILES["app/domain/repositories/history_repository.py"] = '''from abc import ABC, abstractmethod
from typing import List
from ..entities.history import History


class HistoryRepository(ABC):

    @abstractmethod
    def save(self, history: History) -> History: ...

    @abstractmethod
    def find_by_client(self, client_id: str) -> List[History]: ...

    @abstractmethod
    def find_by_card(self, card_id: str) -> List[History]: ...
'''

FILES["app/domain/repositories/seller_repository.py"] = '''from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.seller import Seller


class SellerRepository(ABC):

    @abstractmethod
    def save(self, seller: Seller) -> Seller: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Seller]: ...

    @abstractmethod
    def find_all(self) -> List[Seller]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Seller]: ...
'''

FILES["app/domain/repositories/__init__.py"] = (
    "from .client_repository import ClientRepository\n"
    "from .card_repository import CardRepository\n"
    "from .action_repository import ActionRepository\n"
    "from .history_repository import HistoryRepository\n"
    "from .seller_repository import SellerRepository\n"
)

# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN — Services
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/domain/services/churn_service.py"] = '''from ..repositories.card_repository import CardRepository
from ..repositories.client_repository import ClientRepository
from ..value_objects.card_stage import CardStage


class ChurnService:
    """Domain service: regras de negócio de churn."""

    def __init__(
        self,
        card_repo: CardRepository,
        client_repo: ClientRepository,
    ):
        self._cards = card_repo
        self._clients = client_repo

    def get_total_value_at_risk(self) -> float:
        return self._cards.total_value_at_risk()

    def get_stage_summary(self) -> dict:
        return self._cards.count_by_stage()

    def get_conversion_rate(self) -> float:
        counts = self._cards.count_by_stage()
        total = sum(counts.values())
        if total == 0:
            return 0.0
        converted = counts.get(CardStage.CONVERTED, 0)
        return round((converted / total) * 100, 2)
'''

FILES["app/domain/services/dashboard_service.py"] = '''from ..repositories.card_repository import CardRepository
from ..repositories.client_repository import ClientRepository
from ..repositories.action_repository import ActionRepository
from ..value_objects.card_stage import CardStage


class DashboardService:
    """Agrega indicadores para o dashboard principal."""

    def __init__(
        self,
        card_repo: CardRepository,
        client_repo: ClientRepository,
        action_repo: ActionRepository,
    ):
        self._cards = card_repo
        self._clients = client_repo
        self._actions = action_repo

    def get_indicators(self) -> dict:
        stage_counts = self._cards.count_by_stage()
        total_cards = sum(stage_counts.values())
        clients_at_risk = self._clients.count_at_risk()
        total_value_at_risk = self._cards.total_value_at_risk()

        # Ticket médio dos clientes em risco
        at_risk_clients = self._clients.find_at_risk()
        avg_ticket_at_risk = (
            sum(c.avg_ticket for c in at_risk_clients) / len(at_risk_clients)
            if at_risk_clients
            else 0.0
        )

        return {
            "total_cards": total_cards,
            "clients_at_risk": clients_at_risk,
            "total_value_at_risk": round(total_value_at_risk, 2),
            "avg_ticket_at_risk": round(avg_ticket_at_risk, 2),
            "stage_counts": {k.value: v for k, v in stage_counts.items()},
            "total_opportunities": stage_counts.get(CardStage.IN_NEGOTIATION, 0),
        }
'''

FILES["app/domain/services/performance_service.py"] = '''from ..repositories.card_repository import CardRepository
from ..repositories.action_repository import ActionRepository
from ..value_objects.card_stage import CardStage
from ..value_objects.churn_status import ChurnStatus


class PerformanceService:
    """Métricas de performance por vendedor."""

    def __init__(
        self,
        card_repo: CardRepository,
        action_repo: ActionRepository,
    ):
        self._cards = card_repo
        self._actions = action_repo

    def get_seller_performance(self, seller_id: str) -> dict:
        cards = self._cards.find_by_seller(seller_id)
        actions = self._actions.find_by_seller(seller_id)

        total = len(cards)
        converted = sum(1 for c in cards if c.stage == CardStage.CONVERTED)
        declined = sum(1 for c in cards if c.stage == CardStage.DECLINED)
        in_progress = sum(1 for c in cards if c.stage == CardStage.IN_PROGRESS)
        in_negotiation = sum(1 for c in cards if c.stage == CardStage.IN_NEGOTIATION)

        return {
            "seller_id": seller_id,
            "total_cards": total,
            "converted": converted,
            "declined": declined,
            "in_progress": in_progress,
            "in_negotiation": in_negotiation,
            "conversion_rate": round((converted / total * 100), 2) if total else 0.0,
            "total_actions": len(actions),
        }
'''

FILES["app/domain/services/__init__.py"] = (
    "from .churn_service import ChurnService\n"
    "from .dashboard_service import DashboardService\n"
    "from .performance_service import PerformanceService\n"
)

FILES["app/domain/__init__.py"] = "# domain package\n"


# ══════════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE — Database
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/infrastructure/database/connection.py"] = '''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite only
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from app.infrastructure.database import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
'''

FILES["app/infrastructure/database/models.py"] = '''from sqlalchemy import (
    Column, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base
from app.domain.value_objects.card_stage import CardStage
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.churn_status import ChurnStatus


class SellerModel(Base):
    __tablename__ = "sellers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cards = relationship("CardModel", back_populates="seller")
    actions = relationship("ActionModel", back_populates="seller")


class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    external_id = Column(String, unique=True, nullable=False, index=True)
    ltv = Column(Float, default=0.0)
    avg_ticket = Column(Float, default=0.0)
    last_purchase_date = Column(DateTime, nullable=True)
    churn_risk_score = Column(Float, default=0.0)
    is_at_risk = Column(Boolean, default=False)
    seller_id = Column(String, ForeignKey("sellers.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cards = relationship("CardModel", back_populates="client")
    histories = relationship("HistoryModel", back_populates="client")


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    client_name = Column(String, nullable=False)
    seller_id = Column(String, ForeignKey("sellers.id"), nullable=False)
    stage = Column(SAEnum(CardStage), default=CardStage.BACKLOG, nullable=False)
    title = Column(String, default="")
    description = Column(Text, default="")
    ltv = Column(Float, default=0.0)
    avg_ticket = Column(Float, default=0.0)
    last_purchase_date = Column(DateTime, nullable=True)
    value_at_risk = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("ClientModel", back_populates="cards")
    seller = relationship("SellerModel", back_populates="cards")
    actions = relationship("ActionModel", back_populates="card")
    histories = relationship("HistoryModel", back_populates="card")


class ActionModel(Base):
    __tablename__ = "actions"

    id = Column(String, primary_key=True, index=True)
    card_id = Column(String, ForeignKey("cards.id"), nullable=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    seller_id = Column(String, ForeignKey("sellers.id"), nullable=False)
    action_type = Column(SAEnum(ActionType), nullable=False)
    description = Column(Text, nullable=False)
    outcome = Column(Text, nullable=True)
    status = Column(SAEnum(ChurnStatus), default=ChurnStatus.PENDING)
    scheduled_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    card = relationship("CardModel", back_populates="actions")
    seller = relationship("SellerModel", back_populates="actions")


class HistoryModel(Base):
    __tablename__ = "histories"

    id = Column(String, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    card_id = Column(String, ForeignKey("cards.id"), nullable=True)
    seller_id = Column(String, ForeignKey("sellers.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("ClientModel", back_populates="histories")
    card = relationship("CardModel", back_populates="histories")
'''

FILES["app/infrastructure/database/__init__.py"] = "# database package\n"
FILES["app/infrastructure/database/migrations/__init__.py"] = "# migrations\n"
FILES["app/infrastructure/database/migrations/001_initial.py"] = (
    "# Run create_tables() from connection.py — SQLAlchemy handles DDL.\n"
)

# ══════════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE — Repositories (SQLite)
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/infrastructure/repositories/sqlite_client_repository.py"] = '''import uuid
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
'''

FILES["app/infrastructure/repositories/sqlite_card_repository.py"] = '''from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.value_objects.card_stage import CardStage
from app.infrastructure.database.models import CardModel


def _to_entity(m: CardModel) -> Card:
    return Card(
        id=m.id, client_id=m.client_id, client_name=m.client_name,
        seller_id=m.seller_id, stage=m.stage, title=m.title,
        description=m.description, ltv=m.ltv, avg_ticket=m.avg_ticket,
        last_purchase_date=m.last_purchase_date,
        value_at_risk=m.value_at_risk,
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

    def find_all(self, skip: int = 0, limit: int = 100) -> List[Card]:
        rows = self._db.query(CardModel).offset(skip).limit(limit).all()
        return [_to_entity(r) for r in rows]

    def find_by_seller(self, seller_id: str) -> List[Card]:
        rows = self._db.query(CardModel).filter_by(seller_id=seller_id).all()
        return [_to_entity(r) for r in rows]

    def find_by_stage(self, stage: CardStage) -> List[Card]:
        rows = self._db.query(CardModel).filter_by(stage=stage).all()
        return [_to_entity(r) for r in rows]

    def find_by_client(self, client_id: str) -> List[Card]:
        rows = self._db.query(CardModel).filter_by(client_id=client_id).all()
        return [_to_entity(r) for r in rows]

    def delete(self, id: str) -> bool:
        m = self._db.query(CardModel).filter_by(id=id).first()
        if not m:
            return False
        self._db.delete(m)
        self._db.commit()
        return True

    def count_by_stage(self) -> dict:
        rows = (
            self._db.query(CardModel.stage, func.count(CardModel.id))
            .group_by(CardModel.stage)
            .all()
        )
        return {stage: count for stage, count in rows}

    def total_value_at_risk(self) -> float:
        result = self._db.query(func.sum(CardModel.value_at_risk)).scalar()
        return result or 0.0
'''

FILES["app/infrastructure/repositories/sqlite_action_repository.py"] = '''from typing import Optional, List
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
'''

FILES["app/infrastructure/repositories/sqlite_history_repository.py"] = '''from typing import List
from sqlalchemy.orm import Session

from app.domain.entities.history import History
from app.domain.repositories.history_repository import HistoryRepository
from app.infrastructure.database.models import HistoryModel


def _to_entity(m: HistoryModel) -> History:
    return History(
        id=m.id, client_id=m.client_id, card_id=m.card_id,
        seller_id=m.seller_id, content=m.content, created_at=m.created_at,
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

    def find_by_client(self, client_id: str) -> List[History]:
        rows = (
            self._db.query(HistoryModel)
            .filter_by(client_id=client_id)
            .order_by(HistoryModel.created_at.desc())
            .all()
        )
        return [_to_entity(r) for r in rows]

    def find_by_card(self, card_id: str) -> List[History]:
        rows = (
            self._db.query(HistoryModel)
            .filter_by(card_id=card_id)
            .order_by(HistoryModel.created_at.desc())
            .all()
        )
        return [_to_entity(r) for r in rows]
'''

FILES["app/infrastructure/repositories/sqlite_seller_repository.py"] = '''from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.seller import Seller
from app.domain.repositories.seller_repository import SellerRepository
from app.infrastructure.database.models import SellerModel


def _to_entity(m: SellerModel) -> Seller:
    return Seller(
        id=m.id, name=m.name, email=m.email,
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
'''

FILES["app/infrastructure/repositories/__init__.py"] = "# infra repositories\n"

# ══════════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE — Security / JWT
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/infrastructure/security/jwt_handler.py"] = '''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
'''

FILES["app/infrastructure/security/dependencies.py"] = '''# JWT dependency — login será implementado depois.
# Por ora, todas as rotas são abertas (sem autenticação obrigatória).
# Quando o login for adicionado, injete get_current_user aqui.

from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db


def get_session(db: Session = Depends(get_db)) -> Session:
    return db
'''

FILES["app/infrastructure/security/__init__.py"] = "# security package\n"
FILES["app/infrastructure/__init__.py"] = "# infrastructure package\n"


# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION — DTOs
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/application/dtos/card_dto.py"] = '''from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.value_objects.card_stage import CardStage


@dataclass
class CreateCardDTO:
    client_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0


@dataclass
class UpdateCardDTO:
    title: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[CardStage] = None
    value_at_risk: Optional[float] = None
'''

FILES["app/application/dtos/client_dto.py"] = '''from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UpsertClientDTO:
    external_id: str
    name: str
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0
    seller_id: Optional[str] = None
'''

FILES["app/application/dtos/action_dto.py"] = '''from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.churn_status import ChurnStatus


@dataclass
class CreateActionDTO:
    card_id: str
    client_id: str
    seller_id: str
    action_type: ActionType
    description: str
    scheduled_at: Optional[datetime] = None


@dataclass
class UpdateActionDTO:
    outcome: Optional[str] = None
    status: Optional[ChurnStatus] = None
    completed_at: Optional[datetime] = None
'''

FILES["app/application/dtos/dashboard_dto.py"] = '''from dataclasses import dataclass


@dataclass
class DashboardIndicatorsDTO:
    total_cards: int
    clients_at_risk: int
    total_value_at_risk: float
    avg_ticket_at_risk: float
    stage_counts: dict
    total_opportunities: int
'''

FILES["app/application/dtos/etl_dto.py"] = '''from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class ETLClientRecord:
    external_id: str
    name: str
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0
    seller_id: Optional[str] = None


@dataclass
class ETLCardRecord:
    client_external_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0


@dataclass
class ETLIngestResult:
    created: int = 0
    updated: int = 0
    errors: List[str] = field(default_factory=list)
'''

FILES["app/application/dtos/__init__.py"] = "# dtos package\n"

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION — Use Cases: Cards
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/application/use_cases/cards/create_card.py"] = '''import uuid
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.repositories.client_repository import ClientRepository
from app.application.dtos.card_dto import CreateCardDTO
from app.core.exceptions import EntityNotFoundException


class CreateCardUseCase:

    def __init__(self, card_repo: CardRepository, client_repo: ClientRepository):
        self._cards = card_repo
        self._clients = client_repo

    def execute(self, dto: CreateCardDTO) -> Card:
        client = self._clients.find_by_id(dto.client_id)
        if not client:
            raise EntityNotFoundException(f"Client {dto.client_id} not found")

        card = Card(
            id=str(uuid.uuid4()),
            client_id=client.id,
            client_name=client.name,
            seller_id=dto.seller_id,
            title=dto.title,
            description=dto.description,
            ltv=client.ltv,
            avg_ticket=client.avg_ticket,
            last_purchase_date=client.last_purchase_date,
            value_at_risk=dto.value_at_risk,
        )
        return self._cards.save(card)
'''

FILES["app/application/use_cases/cards/update_card.py"] = '''from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.application.dtos.card_dto import UpdateCardDTO
from app.core.exceptions import EntityNotFoundException


class UpdateCardUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str, dto: UpdateCardDTO) -> Card:
        card = self._cards.find_by_id(card_id)
        if not card:
            raise EntityNotFoundException(f"Card {card_id} not found")

        if dto.title is not None:
            card.title = dto.title
        if dto.description is not None:
            card.description = dto.description
        if dto.stage is not None:
            card.move_to(dto.stage)
        if dto.value_at_risk is not None:
            card.value_at_risk = dto.value_at_risk

        return self._cards.save(card)
'''

FILES["app/application/use_cases/cards/delete_card.py"] = '''from app.domain.repositories.card_repository import CardRepository
from app.core.exceptions import EntityNotFoundException


class DeleteCardUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str) -> bool:
        if not self._cards.find_by_id(card_id):
            raise EntityNotFoundException(f"Card {card_id} not found")
        return self._cards.delete(card_id)
'''

FILES["app/application/use_cases/cards/list_cards.py"] = '''from typing import List, Optional
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.value_objects.card_stage import CardStage


class ListCardsUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(
        self,
        seller_id: Optional[str] = None,
        stage: Optional[CardStage] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Card]:
        if seller_id:
            return self._cards.find_by_seller(seller_id)
        if stage:
            return self._cards.find_by_stage(stage)
        return self._cards.find_all(skip=skip, limit=limit)
'''

FILES["app/application/use_cases/cards/get_card.py"] = '''from typing import Optional
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.core.exceptions import EntityNotFoundException


class GetCardUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str) -> Card:
        card = self._cards.find_by_id(card_id)
        if not card:
            raise EntityNotFoundException(f"Card {card_id} not found")
        return card
'''

FILES["app/application/use_cases/cards/move_card_stage.py"] = '''from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.value_objects.card_stage import CardStage
from app.core.exceptions import EntityNotFoundException


class MoveCardStageUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str, new_stage: CardStage) -> Card:
        card = self._cards.find_by_id(card_id)
        if not card:
            raise EntityNotFoundException(f"Card {card_id} not found")
        card.move_to(new_stage)
        return self._cards.save(card)
'''

FILES["app/application/use_cases/cards/__init__.py"] = "# cards use cases\n"

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION — Use Cases: Clients
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/application/use_cases/clients/list_clients.py"] = '''from typing import List
from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository


class ListClientsUseCase:

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self._clients.find_all(skip=skip, limit=limit)
'''

FILES["app/application/use_cases/clients/get_client.py"] = '''from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository
from app.core.exceptions import EntityNotFoundException


class GetClientUseCase:

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, client_id: str) -> Client:
        client = self._clients.find_by_id(client_id)
        if not client:
            raise EntityNotFoundException(f"Client {client_id} not found")
        return client
'''

FILES["app/application/use_cases/clients/search_clients.py"] = '''from typing import List
from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository


class SearchClientsUseCase:

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, query: str) -> List[Client]:
        return self._clients.search(query)
'''

FILES["app/application/use_cases/clients/get_client_history.py"] = '''from typing import List
from app.domain.entities.history import History
from app.domain.repositories.history_repository import HistoryRepository
from app.domain.repositories.client_repository import ClientRepository
from app.core.exceptions import EntityNotFoundException


class GetClientHistoryUseCase:

    def __init__(
        self,
        history_repo: HistoryRepository,
        client_repo: ClientRepository,
    ):
        self._histories = history_repo
        self._clients = client_repo

    def execute(self, client_id: str) -> List[History]:
        if not self._clients.find_by_id(client_id):
            raise EntityNotFoundException(f"Client {client_id} not found")
        return self._histories.find_by_client(client_id)
'''

FILES["app/application/use_cases/clients/__init__.py"] = "# clients use cases\n"

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION — Use Cases: Actions
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/application/use_cases/actions/register_action.py"] = '''import uuid
from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository
from app.domain.repositories.history_repository import HistoryRepository
from app.domain.entities.history import History
from app.application.dtos.action_dto import CreateActionDTO


class RegisterActionUseCase:

    def __init__(
        self,
        action_repo: ActionRepository,
        history_repo: HistoryRepository,
    ):
        self._actions = action_repo
        self._histories = history_repo

    def execute(self, dto: CreateActionDTO) -> Action:
        action = Action(
            id=str(uuid.uuid4()),
            card_id=dto.card_id,
            client_id=dto.client_id,
            seller_id=dto.seller_id,
            action_type=dto.action_type,
            description=dto.description,
            scheduled_at=dto.scheduled_at,
        )
        saved = self._actions.save(action)

        # Registra no histórico do cliente automaticamente
        history = History(
            id=str(uuid.uuid4()),
            client_id=dto.client_id,
            card_id=dto.card_id,
            seller_id=dto.seller_id,
            content=f"[{dto.action_type.value.upper()}] {dto.description}",
        )
        self._histories.save(history)

        return saved
'''

FILES["app/application/use_cases/actions/list_actions.py"] = '''from typing import List, Optional
from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository


class ListActionsUseCase:

    def __init__(self, action_repo: ActionRepository):
        self._actions = action_repo

    def execute(
        self,
        card_id: Optional[str] = None,
        seller_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Action]:
        if card_id:
            return self._actions.find_by_card(card_id)
        if seller_id:
            return self._actions.find_by_seller(seller_id)
        return self._actions.find_all(skip=skip, limit=limit)
'''

FILES["app/application/use_cases/actions/update_action.py"] = '''from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository
from app.application.dtos.action_dto import UpdateActionDTO
from app.core.exceptions import EntityNotFoundException
from datetime import datetime


class UpdateActionUseCase:

    def __init__(self, action_repo: ActionRepository):
        self._actions = action_repo

    def execute(self, action_id: str, dto: UpdateActionDTO) -> Action:
        action = self._actions.find_by_id(action_id)
        if not action:
            raise EntityNotFoundException(f"Action {action_id} not found")

        if dto.outcome is not None:
            action.outcome = dto.outcome
        if dto.status is not None:
            action.status = dto.status
        if dto.completed_at is not None:
            action.completed_at = dto.completed_at
        action.updated_at = datetime.utcnow()

        return self._actions.save(action)
'''

FILES["app/application/use_cases/actions/__init__.py"] = "# actions use cases\n"

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION — Use Cases: Dashboard
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/application/use_cases/dashboard/get_dashboard_indicators.py"] = '''from app.domain.services.dashboard_service import DashboardService


class GetDashboardIndicatorsUseCase:

    def __init__(self, dashboard_service: DashboardService):
        self._service = dashboard_service

    def execute(self) -> dict:
        return self._service.get_indicators()
'''

FILES["app/application/use_cases/dashboard/get_performance_metrics.py"] = '''from app.domain.services.performance_service import PerformanceService


class GetPerformanceMetricsUseCase:

    def __init__(self, performance_service: PerformanceService):
        self._service = performance_service

    def execute(self, seller_id: str) -> dict:
        return self._service.get_seller_performance(seller_id)
'''

FILES["app/application/use_cases/dashboard/__init__.py"] = "# dashboard use cases\n"

# ══════════════════════════════════════════════════════════════════════════════
# APPLICATION — Use Cases: ETL
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/application/use_cases/etl/ingest_clients.py"] = '''import uuid
from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository
from app.application.dtos.etl_dto import ETLClientRecord, ETLIngestResult


class IngestClientsUseCase:
    """Recebe lista de clientes via ETL e faz upsert."""

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, records: list[ETLClientRecord]) -> ETLIngestResult:
        result = ETLIngestResult()
        for rec in records:
            try:
                existing = self._clients.find_by_external_id(rec.external_id)
                if existing:
                    existing.name = rec.name
                    existing.ltv = rec.ltv
                    existing.avg_ticket = rec.avg_ticket
                    existing.last_purchase_date = rec.last_purchase_date
                    existing.mark_at_risk(rec.churn_risk_score)
                    existing.seller_id = rec.seller_id
                    self._clients.save(existing)
                    result.updated += 1
                else:
                    client = Client(
                        id=str(uuid.uuid4()),
                        name=rec.name,
                        external_id=rec.external_id,
                        ltv=rec.ltv,
                        avg_ticket=rec.avg_ticket,
                        last_purchase_date=rec.last_purchase_date,
                        seller_id=rec.seller_id,
                    )
                    client.mark_at_risk(rec.churn_risk_score)
                    self._clients.save(client)
                    result.created += 1
            except Exception as e:
                result.errors.append(f"{rec.external_id}: {str(e)}")
        return result
'''

FILES["app/application/use_cases/etl/ingest_cards.py"] = '''import uuid
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.repositories.client_repository import ClientRepository
from app.application.dtos.etl_dto import ETLCardRecord, ETLIngestResult


class IngestCardsUseCase:
    """Cria cards automaticamente a partir de dados ETL."""

    def __init__(
        self,
        card_repo: CardRepository,
        client_repo: ClientRepository,
    ):
        self._cards = card_repo
        self._clients = client_repo

    def execute(self, records: list[ETLCardRecord]) -> ETLIngestResult:
        result = ETLIngestResult()
        for rec in records:
            try:
                client = self._clients.find_by_external_id(rec.client_external_id)
                if not client:
                    result.errors.append(
                        f"Client external_id={rec.client_external_id} not found"
                    )
                    continue

                card = Card(
                    id=str(uuid.uuid4()),
                    client_id=client.id,
                    client_name=client.name,
                    seller_id=rec.seller_id,
                    title=rec.title,
                    description=rec.description,
                    ltv=client.ltv,
                    avg_ticket=client.avg_ticket,
                    last_purchase_date=client.last_purchase_date,
                    value_at_risk=rec.value_at_risk,
                )
                self._cards.save(card)
                result.created += 1
            except Exception as e:
                result.errors.append(f"{rec.client_external_id}: {str(e)}")
        return result
'''

FILES["app/application/use_cases/etl/__init__.py"] = "# etl use cases\n"
FILES["app/application/use_cases/__init__.py"] = "# use cases\n"
FILES["app/application/__init__.py"] = "# application package\n"


# ══════════════════════════════════════════════════════════════════════════════
# API — Schemas (Pydantic)
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/api/v1/schemas/common.py"] = '''from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "OK"


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: List[T] = []
    total: int = 0
    skip: int = 0
    limit: int = 100
'''

FILES["app/api/v1/schemas/seller_schema.py"] = '''from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class SellerCreate(BaseModel):
    name: str
    email: EmailStr


class SellerResponse(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
'''

FILES["app/api/v1/schemas/client_schema.py"] = '''from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClientResponse(BaseModel):
    id: str
    name: str
    external_id: str
    ltv: float
    avg_ticket: float
    last_purchase_date: Optional[datetime]
    churn_risk_score: float
    is_at_risk: bool
    seller_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
'''

FILES["app/api/v1/schemas/card_schema.py"] = '''from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.domain.value_objects.card_stage import CardStage


class CardCreate(BaseModel):
    client_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[CardStage] = None
    value_at_risk: Optional[float] = None


class CardMoveStage(BaseModel):
    stage: CardStage


class CardResponse(BaseModel):
    id: str
    client_id: str
    client_name: str
    seller_id: str
    stage: CardStage
    title: str
    description: str
    ltv: float
    avg_ticket: float
    last_purchase_date: Optional[datetime]
    value_at_risk: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
'''

FILES["app/api/v1/schemas/action_schema.py"] = '''from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.churn_status import ChurnStatus


class ActionCreate(BaseModel):
    card_id: str
    client_id: str
    seller_id: str
    action_type: ActionType
    description: str
    scheduled_at: Optional[datetime] = None


class ActionUpdate(BaseModel):
    outcome: Optional[str] = None
    status: Optional[ChurnStatus] = None
    completed_at: Optional[datetime] = None


class ActionResponse(BaseModel):
    id: str
    card_id: str
    client_id: str
    seller_id: str
    action_type: ActionType
    description: str
    outcome: Optional[str]
    status: ChurnStatus
    scheduled_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
'''

FILES["app/api/v1/schemas/dashboard_schema.py"] = '''from pydantic import BaseModel
from typing import Dict


class DashboardIndicators(BaseModel):
    total_cards: int
    clients_at_risk: int
    total_value_at_risk: float
    avg_ticket_at_risk: float
    stage_counts: Dict[str, int]
    total_opportunities: int


class PerformanceMetrics(BaseModel):
    seller_id: str
    total_cards: int
    converted: int
    declined: int
    in_progress: int
    in_negotiation: int
    conversion_rate: float
    total_actions: int
'''

FILES["app/api/v1/schemas/etl_schema.py"] = '''from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ETLClientIn(BaseModel):
    external_id: str
    name: str
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0
    seller_id: Optional[str] = None


class ETLCardIn(BaseModel):
    client_external_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0


class ETLIngestResponse(BaseModel):
    created: int
    updated: int
    errors: List[str]
'''

FILES["app/api/v1/schemas/__init__.py"] = "# schemas\n"

# ══════════════════════════════════════════════════════════════════════════════
# API — Routers
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/api/v1/routers/sellers.py"] = '''import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_seller_repository import SQLiteSellerRepository
from app.domain.entities.seller import Seller
from app.api.v1.schemas.seller_schema import SellerCreate, SellerResponse

router = APIRouter(prefix="/sellers", tags=["Sellers"])


def _repo(db: Session = Depends(get_db)):
    return SQLiteSellerRepository(db)


@router.get("/", response_model=List[SellerResponse])
def list_sellers(repo: SQLiteSellerRepository = Depends(_repo)):
    sellers = repo.find_all()
    return [s.__dict__ for s in sellers]


@router.post("/", response_model=SellerResponse, status_code=201)
def create_seller(body: SellerCreate, repo: SQLiteSellerRepository = Depends(_repo)):
    if repo.find_by_email(body.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    seller = Seller(id=str(uuid.uuid4()), name=body.name, email=body.email)
    saved = repo.save(seller)
    return saved.__dict__
'''

FILES["app/api/v1/routers/clients.py"] = '''from fastapi import APIRouter, Depends, Query
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
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    repo=Depends(_client_repo),
):
    if search:
        clients = SearchClientsUseCase(repo).execute(search)
    else:
        clients = ListClientsUseCase(repo).execute(skip=skip, limit=limit)
    return [c.__dict__ for c in clients]


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: str, repo=Depends(_client_repo)):
    try:
        client = GetClientUseCase(repo).execute(client_id)
        return client.__dict__
    except EntityNotFoundException:
        raise not_found("Client", client_id)


@router.get("/{client_id}/history")
def get_client_history(
    client_id: str,
    client_repo=Depends(_client_repo),
    history_repo=Depends(_history_repo),
):
    try:
        histories = GetClientHistoryUseCase(history_repo, client_repo).execute(client_id)
        return [h.__dict__ for h in histories]
    except EntityNotFoundException:
        raise not_found("Client", client_id)
'''

FILES["app/api/v1/routers/cards.py"] = '''from fastapi import APIRouter, Depends, Query
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
    seller_id: Optional[str] = Query(None),
    stage: Optional[CardStage] = Query(None),
    skip: int = 0,
    limit: int = 100,
    card_repo=Depends(_card_repo),
):
    cards = ListCardsUseCase(card_repo).execute(
        seller_id=seller_id, stage=stage, skip=skip, limit=limit
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
    except EntityNotFoundException as e:
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
'''

FILES["app/api/v1/routers/actions.py"] = '''from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_action_repository import SQLiteActionRepository
from app.infrastructure.repositories.sqlite_history_repository import SQLiteHistoryRepository
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


@router.get("/", response_model=List[ActionResponse])
def list_actions(
    card_id: Optional[str] = Query(None),
    seller_id: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    action_repo=Depends(_action_repo),
):
    actions = ListActionsUseCase(action_repo).execute(
        card_id=card_id, seller_id=seller_id, skip=skip, limit=limit
    )
    return [a.__dict__ for a in actions]


@router.post("/", response_model=ActionResponse, status_code=201)
def register_action(
    body: ActionCreate,
    action_repo=Depends(_action_repo),
    history_repo=Depends(_history_repo),
):
    dto = CreateActionDTO(**body.model_dump())
    action = RegisterActionUseCase(action_repo, history_repo).execute(dto)
    return action.__dict__


@router.patch("/{action_id}", response_model=ActionResponse)
def update_action(
    action_id: str,
    body: ActionUpdate,
    action_repo=Depends(_action_repo),
):
    try:
        dto = UpdateActionDTO(**body.model_dump(exclude_none=True))
        return UpdateActionUseCase(action_repo).execute(action_id, dto).__dict__
    except EntityNotFoundException:
        raise not_found("Action", action_id)


@router.delete("/{action_id}", status_code=204)
def delete_action(action_id: str, action_repo=Depends(_action_repo)):
    repo = action_repo
    if not repo.find_by_id(action_id):
        raise not_found("Action", action_id)
    repo.delete(action_id)
'''

FILES["app/api/v1/routers/dashboard.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.infrastructure.repositories.sqlite_client_repository import SQLiteClientRepository
from app.infrastructure.repositories.sqlite_action_repository import SQLiteActionRepository
from app.domain.services.dashboard_service import DashboardService
from app.application.use_cases.dashboard.get_dashboard_indicators import GetDashboardIndicatorsUseCase
from app.api.v1.schemas.dashboard_schema import DashboardIndicators

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/indicators", response_model=DashboardIndicators)
def get_indicators(db: Session = Depends(get_db)):
    card_repo = SQLiteCardRepository(db)
    client_repo = SQLiteClientRepository(db)
    action_repo = SQLiteActionRepository(db)
    service = DashboardService(card_repo, client_repo, action_repo)
    return GetDashboardIndicatorsUseCase(service).execute()
'''

FILES["app/api/v1/routers/performance.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.infrastructure.repositories.sqlite_action_repository import SQLiteActionRepository
from app.domain.services.performance_service import PerformanceService
from app.application.use_cases.dashboard.get_performance_metrics import GetPerformanceMetricsUseCase
from app.api.v1.schemas.dashboard_schema import PerformanceMetrics

router = APIRouter(prefix="/performance", tags=["Performance"])


@router.get("/{seller_id}", response_model=PerformanceMetrics)
def get_seller_performance(seller_id: str, db: Session = Depends(get_db)):
    card_repo = SQLiteCardRepository(db)
    action_repo = SQLiteActionRepository(db)
    service = PerformanceService(card_repo, action_repo)
    return GetPerformanceMetricsUseCase(service).execute(seller_id)
'''

FILES["app/api/v1/routers/etl.py"] = '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_client_repository import SQLiteClientRepository
from app.infrastructure.repositories.sqlite_card_repository import SQLiteCardRepository
from app.application.use_cases.etl.ingest_clients import IngestClientsUseCase
from app.application.use_cases.etl.ingest_cards import IngestCardsUseCase
from app.application.dtos.etl_dto import ETLClientRecord, ETLCardRecord
from app.api.v1.schemas.etl_schema import ETLClientIn, ETLCardIn, ETLIngestResponse

router = APIRouter(prefix="/etl", tags=["ETL"])


@router.post("/clients", response_model=ETLIngestResponse)
def ingest_clients(payload: List[ETLClientIn], db: Session = Depends(get_db)):
    repo = SQLiteClientRepository(db)
    records = [ETLClientRecord(**item.model_dump()) for item in payload]
    result = IngestClientsUseCase(repo).execute(records)
    return {"created": result.created, "updated": result.updated, "errors": result.errors}


@router.post("/cards", response_model=ETLIngestResponse)
def ingest_cards(payload: List[ETLCardIn], db: Session = Depends(get_db)):
    card_repo = SQLiteCardRepository(db)
    client_repo = SQLiteClientRepository(db)
    records = [ETLCardRecord(**item.model_dump()) for item in payload]
    result = IngestCardsUseCase(card_repo, client_repo).execute(records)
    return {"created": result.created, "updated": result.updated, "errors": result.errors}
'''

FILES["app/api/v1/routers/__init__.py"] = "# routers\n"
FILES["app/api/v1/__init__.py"] = "# api v1\n"
FILES["app/api/__init__.py"] = "# api\n"

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

FILES["app/main.py"] = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.core.config import settings
from app.core.logging import logger
from app.infrastructure.database.connection import create_tables
from app.api.v1.routers import cards, clients, actions, dashboard, performance, etl, sellers

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Athena CRM — Churn Management Suite\\n\\n"
        "API para controle de fluxo de churn, gestão de cards Kanban, "
        "indicadores de risco e ingestão de dados via ETL.\\n\\n"
        "Desenvolvido pela **O2 Data**."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(sellers.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(cards.router, prefix="/api/v1")
app.include_router(actions.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(performance.router, prefix="/api/v1")
app.include_router(etl.router, prefix="/api/v1")

# ── Static Frontend ───────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    logger.info("Starting Athena CRM...")
    create_tables()
    logger.info("Database tables ready.")
    logger.info(f"Docs: http://localhost:8000/docs")
    logger.info(f"ReDoc: http://localhost:8000/redoc")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
'''

FILES["app/__init__.py"] = "# athena crm app\n"

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG FILES
# ══════════════════════════════════════════════════════════════════════════════

FILES["requirements.txt"] = """fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
aiosqlite==0.20.0
"""

FILES["requirements-dev.txt"] = """pytest==8.2.0
pytest-asyncio==0.23.6
httpx==0.27.0
"""

FILES[".env.example"] = """DEBUG=true
DATABASE_URL=sqlite:///./athena_crm.db
SECRET_KEY=change-me-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
"""

FILES["pytest.ini"] = """[pytest]
asyncio_mode = auto
testpaths = tests
"""

FILES["Makefile"] = """install:
\tpip install -r requirements.txt

dev:
\tuvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
\tpytest

lint:
\truff check app/
"""

# ══════════════════════════════════════════════════════════════════════════════
# WRITER
# ══════════════════════════════════════════════════════════════════════════════

def write_files():
    print("=" * 60)
    print("  Athena CRM — Populando arquivos do backend")
    print("=" * 60)
    ok = 0
    for rel_path, content in FILES.items():
        full_path = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅  {full_path}")
        ok += 1
    print()
    print(f"  {ok} arquivos escritos com sucesso!")
    print("=" * 60)
    print()
    print("  Para rodar:")
    print("  cd athena-crm/backend")
    print("  pip install -r requirements.txt")
    print("  uvicorn app.main:app --reload")
    print()


if __name__ == "__main__":
    write_files()

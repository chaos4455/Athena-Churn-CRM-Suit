from sqlalchemy import (
    Column, String, Float, Boolean, DateTime, ForeignKey, Text,
    Enum as SAEnum, Index
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base
from app.domain.value_objects.card_stage import CardStage
from app.domain.value_objects.action_type import ActionType
from app.domain.value_objects.churn_status import ChurnStatus
from app.domain.entities.seller import SellerRole


class SellerModel(Base):
    __tablename__ = "sellers"

    id         = Column(String, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    role       = Column(SAEnum(SellerRole), default=SellerRole.SELLER, nullable=False)
    branch     = Column(String, nullable=True, index=True)
    state      = Column(String(2), nullable=True, index=True)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cards   = relationship("CardModel",   back_populates="seller")
    actions = relationship("ActionModel", back_populates="seller")


class ClientModel(Base):
    __tablename__ = "clients"

    id                 = Column(String, primary_key=True, index=True)
    name               = Column(String, nullable=False, index=True)
    external_id        = Column(String, unique=True, nullable=False, index=True)
    ltv                = Column(Float, default=0.0)
    avg_ticket         = Column(Float, default=0.0)
    last_purchase_date = Column(DateTime, nullable=True)
    churn_risk_score   = Column(Float, default=0.0)
    is_at_risk         = Column(Boolean, default=False, index=True)
    seller_id          = Column(String, ForeignKey("sellers.id"), nullable=True)
    branch             = Column(String, nullable=True, index=True)
    state              = Column(String(2), nullable=True, index=True)
    created_at         = Column(DateTime, default=datetime.utcnow)
    updated_at         = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cards     = relationship("CardModel",    back_populates="client")
    histories = relationship("HistoryModel", back_populates="client")


class CardModel(Base):
    __tablename__ = "cards"

    id                 = Column(String, primary_key=True, index=True)
    client_id          = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    client_name        = Column(String, nullable=False)
    seller_id          = Column(String, ForeignKey("sellers.id"), nullable=False, index=True)
    seller_name        = Column(String, default="")
    stage              = Column(SAEnum(CardStage), default=CardStage.BACKLOG, nullable=False, index=True)
    title              = Column(String, default="")
    description        = Column(Text, default="")
    ltv                = Column(Float, default=0.0)
    avg_ticket         = Column(Float, default=0.0)
    last_purchase_date = Column(DateTime, nullable=True)
    value_at_risk      = Column(Float, default=0.0)
    branch             = Column(String, nullable=True, index=True)
    state              = Column(String(2), nullable=True, index=True)
    cycle_id           = Column(String, nullable=True, index=True)   # "2025-01"
    is_archived        = Column(Boolean, default=False, index=True)
    archived_at        = Column(DateTime, nullable=True)
    created_at         = Column(DateTime, default=datetime.utcnow)
    updated_at         = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client    = relationship("ClientModel",  back_populates="cards")
    seller    = relationship("SellerModel",  back_populates="cards")
    actions   = relationship("ActionModel",  back_populates="card")
    histories = relationship("HistoryModel", back_populates="card")

    __table_args__ = (
        Index("ix_cards_branch_state", "branch", "state"),
        Index("ix_cards_cycle_archived", "cycle_id", "is_archived"),
    )


class ActionModel(Base):
    __tablename__ = "actions"

    id           = Column(String, primary_key=True, index=True)
    card_id      = Column(String, ForeignKey("cards.id"), nullable=False, index=True)
    client_id    = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    seller_id    = Column(String, ForeignKey("sellers.id"), nullable=False, index=True)
    action_type  = Column(SAEnum(ActionType), nullable=False)
    description  = Column(Text, nullable=False)
    outcome      = Column(Text, nullable=True)
    status       = Column(SAEnum(ChurnStatus), default=ChurnStatus.PENDING)
    scheduled_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    card   = relationship("CardModel",   back_populates="actions")
    seller = relationship("SellerModel", back_populates="actions")


class HistoryModel(Base):
    __tablename__ = "histories"

    id           = Column(String, primary_key=True, index=True)
    client_id    = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    card_id      = Column(String, ForeignKey("cards.id"), nullable=True, index=True)
    seller_id    = Column(String, ForeignKey("sellers.id"), nullable=False)
    content      = Column(Text, nullable=False)
    history_type = Column(String, default="note")
    card_stage   = Column(String, nullable=True)
    cycle_id     = Column(String, nullable=True, index=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    client = relationship("ClientModel",  back_populates="histories")
    card   = relationship("CardModel",    back_populates="histories")

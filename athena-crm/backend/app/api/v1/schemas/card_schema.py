from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.domain.value_objects.card_stage import CardStage


class CardCreate(BaseModel):
    client_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0
    branch: Optional[str] = None
    state: Optional[str] = None
    cycle_id: Optional[str] = None


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
    seller_name: str
    stage: CardStage
    title: str
    description: str
    ltv: float
    avg_ticket: float
    last_purchase_date: Optional[datetime]
    value_at_risk: float
    branch: Optional[str]
    state: Optional[str]
    cycle_id: Optional[str]
    is_archived: bool
    archived_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

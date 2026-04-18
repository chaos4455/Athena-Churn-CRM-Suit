from dataclasses import dataclass
from typing import Optional
from app.domain.value_objects.card_stage import CardStage


@dataclass
class CreateCardDTO:
    client_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0
    branch: Optional[str] = None
    state: Optional[str] = None
    cycle_id: Optional[str] = None


@dataclass
class UpdateCardDTO:
    title: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[CardStage] = None
    value_at_risk: Optional[float] = None

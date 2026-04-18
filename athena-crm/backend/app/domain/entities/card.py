from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from ..value_objects.card_stage import CardStage


@dataclass
class Card:
    id: str
    client_id: str
    client_name: str
    seller_id: str
    seller_name: str = ""
    stage: CardStage = CardStage.BACKLOG
    title: str = ""
    description: str = ""
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    value_at_risk: float = 0.0
    branch: Optional[str] = None      # filial
    state: Optional[str] = None       # UF
    cycle_id: Optional[str] = None    # ex: "2025-01"
    is_archived: bool = False
    archived_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def move_to(self, stage: CardStage) -> None:
        self.stage = stage
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        self.is_archived = True
        self.archived_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

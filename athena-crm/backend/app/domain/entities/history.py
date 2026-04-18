from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class History:
    id: str
    client_id: str
    card_id: Optional[str]
    seller_id: str
    content: str
    history_type: str = "note"        # note | card_created | card_archived | action | stage_change
    card_stage: Optional[str] = None  # estágio do card no momento
    cycle_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

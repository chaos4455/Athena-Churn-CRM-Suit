from dataclasses import dataclass, field
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

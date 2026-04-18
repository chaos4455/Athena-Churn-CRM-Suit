from dataclasses import dataclass
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

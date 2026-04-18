from pydantic import BaseModel
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

    # enriched — names
    client_name: Optional[str] = None
    card_title:  Optional[str] = None
    seller_name: Optional[str] = None

    # enriched — card current state (the "resultado")
    card_stage:       Optional[str]      = None   # backlog | in_progress | in_negotiation | converted | declined
    card_cycle_id:    Optional[str]      = None   # e.g. "2025-04"
    card_is_archived: Optional[bool]     = None
    card_archived_at: Optional[datetime] = None

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

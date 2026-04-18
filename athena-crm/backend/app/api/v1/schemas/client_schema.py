from pydantic import BaseModel
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
    branch: Optional[str]
    state: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

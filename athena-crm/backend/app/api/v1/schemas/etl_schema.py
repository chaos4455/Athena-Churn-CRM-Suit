from pydantic import BaseModel
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
    branch: Optional[str] = None
    state: Optional[str] = None


class ETLCardIn(BaseModel):
    client_external_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0
    branch: Optional[str] = None
    state: Optional[str] = None
    cycle_id: Optional[str] = None


class ETLIngestResponse(BaseModel):
    created: int
    updated: int
    archived: int = 0
    errors: List[str]

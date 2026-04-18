from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UpsertClientDTO:
    external_id: str
    name: str
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0
    seller_id: Optional[str] = None

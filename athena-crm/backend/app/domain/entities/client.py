from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Client:
    id: str
    name: str
    external_id: str                  # ID no ERP de origem
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0     # 0–100
    is_at_risk: bool = False
    seller_id: Optional[str] = None
    branch: Optional[str] = None      # filial
    state: Optional[str] = None       # UF
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def mark_at_risk(self, score: float) -> None:
        self.churn_risk_score = score
        self.is_at_risk = score >= 60.0
        self.updated_at = datetime.utcnow()

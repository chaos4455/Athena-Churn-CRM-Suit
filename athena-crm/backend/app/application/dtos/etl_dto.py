from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class ETLClientRecord:
    external_id: str
    name: str
    ltv: float = 0.0
    avg_ticket: float = 0.0
    last_purchase_date: Optional[datetime] = None
    churn_risk_score: float = 0.0
    seller_id: Optional[str] = None
    branch: Optional[str] = None
    state: Optional[str] = None


@dataclass
class ETLCardRecord:
    client_external_id: str
    seller_id: str
    title: str
    description: str = ""
    value_at_risk: float = 0.0
    branch: Optional[str] = None
    state: Optional[str] = None
    cycle_id: Optional[str] = None


@dataclass
class ETLIngestResult:
    created: int = 0
    updated: int = 0
    archived: int = 0
    errors: List[str] = field(default_factory=list)

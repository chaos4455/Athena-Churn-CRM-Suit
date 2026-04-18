from pydantic import BaseModel
from typing import Dict, List, Optional


class DashboardIndicators(BaseModel):
    total_cards: int
    clients_at_risk: int
    total_value_at_risk: float
    avg_ticket_at_risk: float
    stage_counts: Dict[str, int]
    total_opportunities: int
    # breakdown
    by_branch: Dict[str, Dict] = {}
    by_state:  Dict[str, Dict] = {}


class PerformanceMetrics(BaseModel):
    seller_id: str
    total_cards: int
    converted: int
    declined: int
    in_progress: int
    in_negotiation: int
    backlog: int
    conversion_rate: float
    total_actions: int


class SellerPerformanceRow(BaseModel):
    seller_id: str
    seller_name: str
    branch: Optional[str]
    state: Optional[str]
    total_cards: int
    converted: int
    declined: int
    in_progress: int
    in_negotiation: int
    conversion_rate: float
    total_actions: int


class TeamPerformance(BaseModel):
    sellers: List[SellerPerformanceRow]
    totals: PerformanceMetrics

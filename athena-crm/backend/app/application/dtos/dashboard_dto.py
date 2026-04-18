from dataclasses import dataclass


@dataclass
class DashboardIndicatorsDTO:
    total_cards: int
    clients_at_risk: int
    total_value_at_risk: float
    avg_ticket_at_risk: float
    stage_counts: dict
    total_opportunities: int

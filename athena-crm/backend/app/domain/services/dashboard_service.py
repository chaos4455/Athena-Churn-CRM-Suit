from typing import Optional
from ..repositories.card_repository import CardRepository
from ..repositories.client_repository import ClientRepository
from ..repositories.action_repository import ActionRepository
from ..value_objects.card_stage import CardStage


class DashboardService:
    """Agrega indicadores para o dashboard — suporta filtros por filial/estado."""

    def __init__(
        self,
        card_repo: CardRepository,
        client_repo: ClientRepository,
        action_repo: ActionRepository,
    ):
        self._cards   = card_repo
        self._clients = client_repo
        self._actions = action_repo

    def get_indicators(
        self,
        branch:    Optional[str] = None,
        state:     Optional[str] = None,
        seller_id: Optional[str] = None,
    ) -> dict:
        stage_counts        = self._cards.count_by_stage(branch=branch, state=state, seller_id=seller_id)
        total_cards         = sum(stage_counts.values())
        total_value_at_risk = self._cards.total_value_at_risk(branch=branch, state=state, seller_id=seller_id)

        at_risk_clients = self._clients.find_at_risk()
        if branch:
            at_risk_clients = [c for c in at_risk_clients if c.branch == branch]
        if state:
            at_risk_clients = [c for c in at_risk_clients if c.state == state]
        # For seller filter: get client_ids from seller's cards
        if seller_id:
            seller_card_client_ids = {
                c.client_id
                for c in self._cards.find_by_seller(seller_id)
            }
            at_risk_clients = [c for c in at_risk_clients if c.id in seller_card_client_ids]

        avg_ticket_at_risk = (
            sum(c.avg_ticket for c in at_risk_clients) / len(at_risk_clients)
            if at_risk_clients else 0.0
        )

        base = {
            "total_cards":         total_cards,
            "clients_at_risk":     len(at_risk_clients),
            "total_value_at_risk": round(total_value_at_risk, 2),
            "avg_ticket_at_risk":  round(avg_ticket_at_risk, 2),
            "stage_counts":        {k.value: v for k, v in stage_counts.items()},
            "total_opportunities": stage_counts.get(CardStage.IN_NEGOTIATION, 0),
            "by_branch":           {},
            "by_state":            {},
        }

        # Breakdown por filial/estado — só quando não há filtro de seller
        # (ou inclui breakdown filtrado por seller quando seller_id está presente)
        for br in self._cards.list_branches():
            sc = self._cards.count_by_stage(branch=br, seller_id=seller_id)
            base["by_branch"][br] = {
                "total_cards":         sum(sc.values()),
                "total_value_at_risk": round(self._cards.total_value_at_risk(branch=br, seller_id=seller_id), 2),
                "stage_counts":        {k.value: v for k, v in sc.items()},
            }
        for st in self._cards.list_states():
            sc = self._cards.count_by_stage(state=st, seller_id=seller_id)
            base["by_state"][st] = {
                "total_cards":         sum(sc.values()),
                "total_value_at_risk": round(self._cards.total_value_at_risk(state=st, seller_id=seller_id), 2),
                "stage_counts":        {k.value: v for k, v in sc.items()},
            }

        return base

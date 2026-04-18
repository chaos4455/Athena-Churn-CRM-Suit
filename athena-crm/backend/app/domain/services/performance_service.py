from typing import Optional
from ..repositories.card_repository import CardRepository
from ..repositories.action_repository import ActionRepository
from ..value_objects.card_stage import CardStage


class PerformanceService:

    def __init__(self, card_repo: CardRepository, action_repo: ActionRepository):
        self._cards   = card_repo
        self._actions = action_repo

    def get_seller_performance(
        self,
        seller_id: str,
        branch:    Optional[str] = None,
        state:     Optional[str] = None,
        archived:  bool          = False,
    ) -> dict:
        cards   = self._cards.find_by_seller(seller_id, archived=archived)
        actions = self._actions.find_by_seller(seller_id)

        # Aplica filtros opcionais
        if branch:
            cards = [c for c in cards if c.branch == branch]
        if state:
            cards = [c for c in cards if c.state == state]

        total        = len(cards)
        converted    = sum(1 for c in cards if c.stage == CardStage.CONVERTED)
        declined     = sum(1 for c in cards if c.stage == CardStage.DECLINED)
        in_progress  = sum(1 for c in cards if c.stage == CardStage.IN_PROGRESS)
        in_neg       = sum(1 for c in cards if c.stage == CardStage.IN_NEGOTIATION)
        backlog      = sum(1 for c in cards if c.stage == CardStage.BACKLOG)

        return {
            "seller_id":       seller_id,
            "total_cards":     total,
            "converted":       converted,
            "declined":        declined,
            "in_progress":     in_progress,
            "in_negotiation":  in_neg,
            "backlog":         backlog,
            "conversion_rate": round(converted / total * 100, 2) if total else 0.0,
            "total_actions":   len(actions),
        }

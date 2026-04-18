from typing import List, Optional
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.value_objects.card_stage import CardStage


class ListCardsUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(
        self,
        seller_id: Optional[str]      = None,
        stage:     Optional[CardStage] = None,
        branch:    Optional[str]      = None,
        state:     Optional[str]      = None,
        cycle_id:  Optional[str]      = None,
        archived:  bool               = False,
        skip:      int                = 0,
        limit:     int                = 200,
    ) -> List[Card]:
        if seller_id:
            return self._cards.find_by_seller(seller_id, archived=archived)
        if stage:
            return self._cards.find_by_stage(stage, archived=archived)
        if branch:
            return self._cards.find_by_branch(branch, archived=archived)
        if state:
            return self._cards.find_by_state(state, archived=archived)
        if cycle_id:
            return self._cards.find_by_cycle(cycle_id)
        return self._cards.find_all(skip=skip, limit=limit, archived=archived)

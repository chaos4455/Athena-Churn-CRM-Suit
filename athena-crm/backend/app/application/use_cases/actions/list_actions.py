from typing import List, Optional
from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository


class ListActionsUseCase:

    def __init__(self, action_repo: ActionRepository):
        self._actions = action_repo

    def execute(
        self,
        card_id: Optional[str] = None,
        seller_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Action]:
        if card_id:
            return self._actions.find_by_card(card_id)
        if seller_id:
            return self._actions.find_by_seller(seller_id)
        return self._actions.find_all(skip=skip, limit=limit)

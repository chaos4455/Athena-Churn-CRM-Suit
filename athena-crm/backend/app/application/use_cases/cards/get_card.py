from typing import Optional
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.core.exceptions import EntityNotFoundException


class GetCardUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str) -> Card:
        card = self._cards.find_by_id(card_id)
        if not card:
            raise EntityNotFoundException(f"Card {card_id} not found")
        return card

from app.domain.repositories.card_repository import CardRepository
from app.core.exceptions import EntityNotFoundException


class DeleteCardUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str) -> bool:
        if not self._cards.find_by_id(card_id):
            raise EntityNotFoundException(f"Card {card_id} not found")
        return self._cards.delete(card_id)

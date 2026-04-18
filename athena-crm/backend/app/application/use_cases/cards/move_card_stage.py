from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.value_objects.card_stage import CardStage
from app.core.exceptions import EntityNotFoundException


class MoveCardStageUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str, new_stage: CardStage) -> Card:
        card = self._cards.find_by_id(card_id)
        if not card:
            raise EntityNotFoundException(f"Card {card_id} not found")
        card.move_to(new_stage)
        return self._cards.save(card)

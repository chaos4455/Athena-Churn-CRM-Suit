from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.application.dtos.card_dto import UpdateCardDTO
from app.core.exceptions import EntityNotFoundException


class UpdateCardUseCase:

    def __init__(self, card_repo: CardRepository):
        self._cards = card_repo

    def execute(self, card_id: str, dto: UpdateCardDTO) -> Card:
        card = self._cards.find_by_id(card_id)
        if not card:
            raise EntityNotFoundException(f"Card {card_id} not found")

        if dto.title is not None:
            card.title = dto.title
        if dto.description is not None:
            card.description = dto.description
        if dto.stage is not None:
            card.move_to(dto.stage)
        if dto.value_at_risk is not None:
            card.value_at_risk = dto.value_at_risk

        return self._cards.save(card)

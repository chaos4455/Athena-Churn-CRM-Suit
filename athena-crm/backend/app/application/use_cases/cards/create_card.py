import uuid
from app.domain.entities.card import Card
from app.domain.repositories.card_repository import CardRepository
from app.domain.repositories.client_repository import ClientRepository
from app.application.dtos.card_dto import CreateCardDTO
from app.core.exceptions import EntityNotFoundException


class CreateCardUseCase:

    def __init__(self, card_repo: CardRepository, client_repo: ClientRepository):
        self._cards   = card_repo
        self._clients = client_repo

    def execute(self, dto: CreateCardDTO) -> Card:
        client = self._clients.find_by_id(dto.client_id)
        if not client:
            raise EntityNotFoundException(f"Client {dto.client_id} not found")

        card = Card(
            id=str(uuid.uuid4()),
            client_id=client.id,
            client_name=client.name,
            seller_id=dto.seller_id,
            title=dto.title,
            description=dto.description,
            ltv=client.ltv,
            avg_ticket=client.avg_ticket,
            last_purchase_date=client.last_purchase_date,
            value_at_risk=dto.value_at_risk,
            branch=dto.branch or client.branch,
            state=dto.state or client.state,
            cycle_id=dto.cycle_id,
        )
        return self._cards.save(card)

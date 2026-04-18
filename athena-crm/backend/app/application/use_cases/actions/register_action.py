import uuid
from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository
from app.domain.repositories.history_repository import HistoryRepository
from app.domain.entities.history import History
from app.application.dtos.action_dto import CreateActionDTO


class RegisterActionUseCase:

    def __init__(
        self,
        action_repo: ActionRepository,
        history_repo: HistoryRepository,
    ):
        self._actions = action_repo
        self._histories = history_repo

    def execute(self, dto: CreateActionDTO) -> Action:
        action = Action(
            id=str(uuid.uuid4()),
            card_id=dto.card_id,
            client_id=dto.client_id,
            seller_id=dto.seller_id,
            action_type=dto.action_type,
            description=dto.description,
            scheduled_at=dto.scheduled_at,
        )
        saved = self._actions.save(action)

        # Registra no histórico do cliente automaticamente
        history = History(
            id=str(uuid.uuid4()),
            client_id=dto.client_id,
            card_id=dto.card_id,
            seller_id=dto.seller_id,
            content=f"[{dto.action_type.value.upper()}] {dto.description}",
        )
        self._histories.save(history)

        return saved

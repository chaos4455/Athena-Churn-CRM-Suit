from app.domain.entities.action import Action
from app.domain.repositories.action_repository import ActionRepository
from app.application.dtos.action_dto import UpdateActionDTO
from app.core.exceptions import EntityNotFoundException
from datetime import datetime


class UpdateActionUseCase:

    def __init__(self, action_repo: ActionRepository):
        self._actions = action_repo

    def execute(self, action_id: str, dto: UpdateActionDTO) -> Action:
        action = self._actions.find_by_id(action_id)
        if not action:
            raise EntityNotFoundException(f"Action {action_id} not found")

        if dto.outcome is not None:
            action.outcome = dto.outcome
        if dto.status is not None:
            action.status = dto.status
        if dto.completed_at is not None:
            action.completed_at = dto.completed_at
        action.updated_at = datetime.utcnow()

        return self._actions.save(action)

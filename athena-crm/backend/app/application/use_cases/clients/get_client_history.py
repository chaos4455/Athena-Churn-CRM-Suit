from typing import List
from app.domain.entities.history import History
from app.domain.repositories.history_repository import HistoryRepository
from app.domain.repositories.client_repository import ClientRepository
from app.core.exceptions import EntityNotFoundException


class GetClientHistoryUseCase:

    def __init__(
        self,
        history_repo: HistoryRepository,
        client_repo: ClientRepository,
    ):
        self._histories = history_repo
        self._clients = client_repo

    def execute(self, client_id: str) -> List[History]:
        if not self._clients.find_by_id(client_id):
            raise EntityNotFoundException(f"Client {client_id} not found")
        return self._histories.find_by_client(client_id)

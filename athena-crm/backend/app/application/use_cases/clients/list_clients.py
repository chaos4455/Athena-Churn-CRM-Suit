from typing import List
from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository


class ListClientsUseCase:

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self._clients.find_all(skip=skip, limit=limit)

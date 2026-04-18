from typing import List
from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository


class SearchClientsUseCase:

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, query: str) -> List[Client]:
        return self._clients.search(query)

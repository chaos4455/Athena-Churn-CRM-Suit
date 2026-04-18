from app.domain.entities.client import Client
from app.domain.repositories.client_repository import ClientRepository
from app.core.exceptions import EntityNotFoundException


class GetClientUseCase:

    def __init__(self, client_repo: ClientRepository):
        self._clients = client_repo

    def execute(self, client_id: str) -> Client:
        client = self._clients.find_by_id(client_id)
        if not client:
            raise EntityNotFoundException(f"Client {client_id} not found")
        return client

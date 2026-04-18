from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.client import Client


class ClientRepository(ABC):

    @abstractmethod
    def save(self, client: Client) -> Client: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Client]: ...

    @abstractmethod
    def find_by_external_id(self, external_id: str) -> Optional[Client]: ...

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]: ...

    @abstractmethod
    def search(self, query: str) -> List[Client]: ...

    @abstractmethod
    def find_at_risk(self) -> List[Client]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def count_at_risk(self) -> int: ...

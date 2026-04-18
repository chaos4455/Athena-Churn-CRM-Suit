from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.action import Action


class ActionRepository(ABC):

    @abstractmethod
    def save(self, action: Action) -> Action: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Action]: ...

    @abstractmethod
    def find_by_card(self, card_id: str) -> List[Action]: ...

    @abstractmethod
    def find_by_client(self, client_id: str) -> List[Action]: ...

    @abstractmethod
    def find_by_seller(self, seller_id: str) -> List[Action]: ...

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Action]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

from abc import ABC, abstractmethod
from typing import List
from ..entities.history import History


class HistoryRepository(ABC):

    @abstractmethod
    def save(self, history: History) -> History: ...

    @abstractmethod
    def find_by_client(self, client_id: str) -> List[History]: ...

    @abstractmethod
    def find_by_card(self, card_id: str) -> List[History]: ...

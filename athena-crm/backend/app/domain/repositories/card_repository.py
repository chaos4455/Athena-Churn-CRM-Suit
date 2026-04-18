from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.card import Card
from ..value_objects.card_stage import CardStage


class CardRepository(ABC):

    @abstractmethod
    def save(self, card: Card) -> Card: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Card]: ...

    @abstractmethod
    def find_all(self, skip: int = 0, limit: int = 200,
                 archived: bool = False) -> List[Card]: ...

    @abstractmethod
    def find_by_seller(self, seller_id: str,
                       archived: bool = False) -> List[Card]: ...

    @abstractmethod
    def find_by_stage(self, stage: CardStage,
                      archived: bool = False) -> List[Card]: ...

    @abstractmethod
    def find_by_client(self, client_id: str) -> List[Card]: ...

    @abstractmethod
    def find_by_branch(self, branch: str,
                       archived: bool = False) -> List[Card]: ...

    @abstractmethod
    def find_by_state(self, state: str,
                      archived: bool = False) -> List[Card]: ...

    @abstractmethod
    def find_by_cycle(self, cycle_id: str) -> List[Card]: ...

    @abstractmethod
    def archive_old_cycles(self, current_cycle_id: str) -> int: ...

    @abstractmethod
    def find_archived_in_cycle_transition(self, current_cycle_id: str) -> List[Card]: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

    @abstractmethod
    def count_by_stage(self, branch: Optional[str] = None,
                       state: Optional[str] = None,
                       archived: bool = False) -> dict: ...

    @abstractmethod
    def total_value_at_risk(self, branch: Optional[str] = None,
                            state: Optional[str] = None) -> float: ...

    @abstractmethod
    def list_branches(self) -> List[str]: ...

    @abstractmethod
    def list_states(self) -> List[str]: ...

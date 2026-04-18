from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.seller import Seller


class SellerRepository(ABC):

    @abstractmethod
    def save(self, seller: Seller) -> Seller: ...

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Seller]: ...

    @abstractmethod
    def find_all(self) -> List[Seller]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Seller]: ...

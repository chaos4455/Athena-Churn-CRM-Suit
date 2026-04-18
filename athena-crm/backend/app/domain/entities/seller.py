from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class SellerRole(str, Enum):
    ADMIN   = "admin"    # vê tudo
    MANAGER = "manager"  # vê filial/estado
    SELLER  = "seller"   # vê apenas seus cards


@dataclass
class Seller:
    id: str
    name: str
    email: str
    role: SellerRole = SellerRole.SELLER
    branch: Optional[str] = None   # filial
    state: Optional[str] = None    # estado (UF)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

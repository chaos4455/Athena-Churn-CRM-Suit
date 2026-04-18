from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.domain.entities.seller import SellerRole


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    role: SellerRole = SellerRole.SELLER
    branch: Optional[str] = None
    state: Optional[str] = None


class SellerResponse(BaseModel):
    id: str
    name: str
    email: str
    role: SellerRole
    branch: Optional[str]
    state: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

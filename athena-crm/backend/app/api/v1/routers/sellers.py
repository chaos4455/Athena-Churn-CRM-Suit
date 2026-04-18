import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlite_seller_repository import SQLiteSellerRepository
from app.domain.entities.seller import Seller
from app.api.v1.schemas.seller_schema import SellerCreate, SellerResponse

router = APIRouter(prefix="/sellers", tags=["Sellers"])


def _repo(db: Session = Depends(get_db)):
    return SQLiteSellerRepository(db)


@router.get("/", response_model=List[SellerResponse])
def list_sellers(repo: SQLiteSellerRepository = Depends(_repo)):
    sellers = repo.find_all()
    return [s.__dict__ for s in sellers]


@router.post("/", response_model=SellerResponse, status_code=201)
def create_seller(body: SellerCreate, repo: SQLiteSellerRepository = Depends(_repo)):
    if repo.find_by_email(body.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    seller = Seller(
        id=str(uuid.uuid4()),
        name=body.name,
        email=body.email,
        role=body.role,
        branch=body.branch,
        state=body.state,
    )
    saved = repo.save(seller)
    return saved.__dict__

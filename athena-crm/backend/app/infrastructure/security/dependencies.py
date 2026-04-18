# JWT dependency — login será implementado depois.
# Por ora, todas as rotas são abertas (sem autenticação obrigatória).
# Quando o login for adicionado, injete get_current_user aqui.

from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import get_db


def get_session(db: Session = Depends(get_db)) -> Session:
    return db

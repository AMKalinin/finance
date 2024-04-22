from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.currency import currency
from app.api import deps
from app import crud


router = APIRouter()


@router.get("/", response_model=list[currency])
def get_currency(db: Session = Depends(deps.get_db)):
    return crud.currency.get_all(db)

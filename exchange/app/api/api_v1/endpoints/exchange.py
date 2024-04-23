from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.exchange import exchange
from app.api import deps
from app import crud


router = APIRouter()


@router.get("/rate", response_model=exchange | None)
def get_exchange_rate(
    *, db: Session = Depends(deps.get_db), from_cur: str, to_cur: str
):
    return crud.ex_rate.get_last_exchange_rate(db, from_cur, to_cur)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.transaction import transaction_in, transaction_out

router = APIRouter()


@router.post("/create", response_model=transaction_out)
def create_transaction(*, db: Session = Depends(deps.get_db), transaction_info: transaction_in):
    return crud.transaction.create_transaction(db, transaction_info)


@router.delete("/{transaction_id}")
def delete_transaction(test: str):
    return {test}

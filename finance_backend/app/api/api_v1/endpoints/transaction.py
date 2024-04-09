from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.account import account_in_balance
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
    transaction_out,
)

router = APIRouter()


@router.get("/all", response_model=list[transaction_out])
def get_all(db: Session = Depends(deps.get_db)):
    return crud.transaction.get_all_transaction(db)


@router.get("/by_type", response_model=list[transaction_out])
def get_all_by_type(*, db: Session = Depends(deps.get_db), operation_type: str):
    return crud.transaction.get_all_transaction_by_type(db, operation_type)


@router.get("/by_period", response_model=list[transaction_out])
def get_all_by_period(*, db: Session = Depends(deps.get_db), from_date: date, to_date: date):
    return crud.transaction.get_all_transaction_for_period(db, from_date, to_date)


@router.get("/by_period_type", response_model=list[transaction_out])
def get_all_by_period_with_type(
    *, db: Session = Depends(deps.get_db), from_date: date, to_date: date, operation_type: str
):
    return crud.transaction.get_all_transaction_for_period_with_type(
        db, from_date, to_date, operation_type
    )


@router.post("/create", response_model=transaction_out)
def create_transaction(*, db: Session = Depends(deps.get_db), transaction_info: transaction_in):
    if transaction_info.type_name == "Debit":
        crud.account.update_balance(
            db,
            account_in_balance(
                id=transaction_info.FROM, operation="minus", balance=transaction_info.size
            ),
        )
    elif transaction_info.type_name == "Transfer":
        crud.account.update_balance(
            db,
            account_in_balance(
                id=transaction_info.FROM, operation="minus", balance=transaction_info.size
            ),
        )
        crud.account.update_balance(
            db,
            account_in_balance(
                id=transaction_info.TO, operation="plus", balance=transaction_info.size
            ),
        )
    elif transaction_info.type_name == "Adding":
        crud.account.update_balance(
            db,
            account_in_balance(
                id=transaction_info.TO, operation="plus", balance=transaction_info.size
            ),
        )
    return crud.transaction.create_transaction(db, transaction_info)


@router.put("/{id}/type", response_model=transaction_out)
def update_type(
    *,
    db: Session = Depends(deps.get_db),
    transaction_info: transaction_in_type = Depends(transaction_in_type),
):
    return crud.transaction.update_type(db, transaction_info)


@router.put("/{id}/date", response_model=transaction_out)
def update_date(
    *,
    db: Session = Depends(deps.get_db),
    transaction_info: transaction_in_date = Depends(transaction_in_date),
):
    return crud.transaction.update_date(db, transaction_info)


@router.put("/{id}/size", response_model=transaction_out)
def update_size(
    *,
    db: Session = Depends(deps.get_db),
    transaction_info: transaction_in_size = Depends(transaction_in_size),
):
    return crud.transaction.update_size(db, transaction_info)


@router.put("/{id}/description", response_model=transaction_out)
def update_description(
    *,
    db: Session = Depends(deps.get_db),
    transaction_info: transaction_in_description = Depends(transaction_in_description),
):
    return crud.transaction.update_description(db, transaction_info)


@router.delete("/{transaction_id}")
def delete_transaction(test: str):
    return {test}

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
    account_out,
)

router = APIRouter()


@router.get("/", response_model=list[account_out])
def get_all_account(db: Session = Depends(deps.get_db)):
    return crud.account.get_all(db)


@router.post("/create", response_model=account_out)
def create_account(*, db: Session = Depends(deps.get_db), account_info: account_in):
    return crud.account.create_account(db, account_info)


@router.get("/{account_id}", response_model=account_out)
def get_account_by_id(*, db: Session = Depends(deps.get_db), account_id: UUID):
    return crud.account.get_by_id(db, account_id)


@router.put("/{id}/balance", response_model=account_out)
def update_balance(
    *,
    db: Session = Depends(deps.get_db),
    account_info: account_in_balance = Depends(account_in_balance),
):
    return crud.account.update_balance(db, account_info)


@router.put("/{id}/name", response_model=account_out)
def update_name(
    *, db: Session = Depends(deps.get_db), account_info: account_in_name = Depends(account_in_name)
):
    return crud.account.update_name(db, account_info)


@router.put("/{id}/description", response_model=account_out)
def update_description(
    *,
    db: Session = Depends(deps.get_db),
    account_info: account_in_description = Depends(account_in_description),
):
    return crud.account.update_description(db, account_info)


@router.delete("/{account_id}")
def delete_account(test: str):
    return {test}

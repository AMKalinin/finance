from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.account import account_in_balance
from app.schemas.transaction import (
    transaction_in,
    transaction_in_date,
    transaction_in_delete,
    transaction_in_description,
    transaction_in_size,
    transaction_in_type,
    transaction_out,
)
from app.service.fin_app import Fin_app

router = APIRouter()


@router.get("/all", response_model=list[transaction_out])
def get_all(fin_app: Fin_app = Depends(deps.get_fin_service)):
    return fin_app.get_all_transaction()  # crud.transaction.get_all_transaction(db)


@router.get("/by_type", response_model=list[transaction_out])
def get_all_by_type(*, fin_app: Fin_app = Depends(deps.get_fin_service), operation_type: str):
    return fin_app.get_all_transaction_by_type(operation_type)


@router.get("/by_period", response_model=list[transaction_out])
def get_all_by_period(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), from_date: date, to_date: date
):
    return fin_app.get_all_transaction_for_period(from_date, to_date)


@router.get("/by_period_type", response_model=list[transaction_out])
def get_all_by_period_with_type(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    from_date: date,
    to_date: date,
    operation_type: str,
):
    return fin_app.get_all_transaction_for_period_with_type(from_date, to_date, operation_type)


@router.post("/create", response_model=transaction_out)
def create_transaction(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), transaction_info: transaction_in
):
    print(transaction_info)
    return fin_app.create_transaction(transaction_info)


# @router.put("/{id}/type", response_model=transaction_out)
def update_type(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    transaction_info: transaction_in_type = Depends(transaction_in_type),
):
    return fin_app.update_transaction_type(transaction_info)


@router.put("/{id}/date", response_model=transaction_out)
def update_date(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    transaction_info: transaction_in_date = Depends(transaction_in_date),
):
    return fin_app.update_transaction_date(transaction_info)


@router.put("/{id}/size", response_model=transaction_out)
def update_size(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    transaction_info: transaction_in_size = Depends(transaction_in_size),
):
    return fin_app.update_transaction_size(transaction_info)


@router.put("/{id}/description", response_model=transaction_out)
def update_description(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    transaction_info: transaction_in_description = Depends(transaction_in_description),
):
    return fin_app.update_transaction_description(transaction_info)


@router.delete("/{id}", response_model=transaction_out)
def delete_transaction(*, fin_app: Fin_app = Depends(deps.get_fin_service), id: UUID):
    return fin_app.delete_transaction(id)

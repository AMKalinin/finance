from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
    account_out,
)
from app.service.fin_app import Fin_app

router = APIRouter()


@router.get("/", response_model=list[account_out])
def get_all_account(fin_app: Fin_app = Depends(deps.get_fin_service)):
    return fin_app.get_all_account()


@router.post("/create", response_model=account_out)
def create_account(*, fin_app: Fin_app = Depends(deps.get_fin_service), account_info: account_in):
    return fin_app.create_account(account_info)


@router.get("/{account_id}", response_model=account_out)
def get_account_by_id(*, fin_app: Fin_app = Depends(deps.get_fin_service), account_id: UUID):
    return fin_app.get_account_by_id(account_id)


# @router.put("/{id}/balance", response_model=account_out)
def update_balance(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_balance = Depends(account_in_balance),
):
    return fin_app.update_account_balance(account_info)


@router.put("/{id}/name", response_model=account_out)
def update_name(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_name = Depends(account_in_name),
):
    return fin_app.update_account_name(account_info)


@router.put("/{id}/description", response_model=account_out)
def update_description(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_description = Depends(account_in_description),
):
    return fin_app.update_account_description(account_info)


#
# @router.delete("/{account_id}")
# def delete_account(test: str):
#     return {test}

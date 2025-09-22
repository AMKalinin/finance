from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.account import (
    account_in,
    account_in_balance,
    account_in_description,
    account_in_name,
    account_in_interest_rate,
    account_in_archived,
    account_in_decimal_places,
    account_in_emergency_fund,
    account_in_primary,
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


@router.get("/{id}", response_model=account_out)
def get_account_by_id(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    id: UUID
):
    return fin_app.get_account_by_id(id)


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

@router.put("/{id}/interest_rate", response_model=account_out)
def update_interest_rate(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_interest_rate = Depends(account_in_interest_rate),
):
    return fin_app.update_account_interest_rate(account_info)

@router.put("/{id}/emergency_fund", response_model=account_out)
def update_emergency_fund(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_emergency_fund = Depends(account_in_emergency_fund),
):
    return fin_app.update_account_emergency_fund(account_info)

@router.put("/{id}/decimal_places", response_model=account_out)
def update_decimal_places(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_decimal_places = Depends(account_in_decimal_places),
):
    return fin_app.update_account_decimal_places(account_info)

@router.put("/{id}/archived", response_model=account_out)
def update_archived(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_archived = Depends(account_in_archived),
):
    return fin_app.update_account_archived(account_info)

@router.put("/{id}/primary", response_model=account_out)
def update_primary(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    account_info: account_in_primary = Depends(account_in_primary),
):
    return fin_app.update_account_primary(account_info)


@router.delete("/{id}", response_model=account_out)
def delete_account(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    id:UUID,
):
    return fin_app.delete_account(id)

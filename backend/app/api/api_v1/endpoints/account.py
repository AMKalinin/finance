from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

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
    account_update_in,
)
from app.service.fin_app import Fin_app
from app.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


class PaginationParams(BaseModel):
    """Параметры пагинации."""
    skip: int = Field(default=0, ge=0, description="Количество записей для пропуска")
    limit: int = Field(default=100, le=1000, description="Максимальное количество записей (макс. 1000)")


class PaginatedResponse(BaseModel):
    """Общий ответ с пагинацией."""
    items: List[account_out]
    total: int
    skip: int
    limit: int
    has_more: bool = Field(default=False, description="Есть ли еще записи")


@router.get("/", response_model=PaginatedResponse)
def get_all_account(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip", description="Пропустить N записей"),
    limit: int = Query(100, ge=1, le=1000, alias="limit", description="Максимум N записей")
):
    """
    Получить все учетные записи с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска (по умолчанию 0)
        limit: Максимальное количество записей (макс. 1000, по умолчанию 100)
    """
    logger.info(f"Получение списка счетов с пагинацией", extra={"skip": skip, "limit": limit})
    
    accounts = fin_app.get_all_account(skip=skip, limit=limit)
    total_count = fin_app.get_total_accounts()
    has_more = (skip + limit) < total_count
    
    return PaginatedResponse(
        items=accounts,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )


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


@router.patch("/{id}")
def update_account(*, fin_app:Fin_app=Depends(deps.get_fin_service), account_info: account_update_in):
    return fin_app.update_account(account_info)

# @router.put("/{id}/name", response_model=account_out)
# def update_name(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_name = Depends(account_in_name),
# ):
#     return fin_app.update_account_name(account_info)
#
#
# @router.put("/{id}/description", response_model=account_out)
# def update_description(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_description = Depends(account_in_description),
# ):
#     return fin_app.update_account_description(account_info)
#
# @router.put("/{id}/interest_rate", response_model=account_out)
# def update_interest_rate(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_interest_rate = Depends(account_in_interest_rate),
# ):
#     return fin_app.update_account_interest_rate(account_info)
#
# @router.put("/{id}/emergency_fund", response_model=account_out)
# def update_emergency_fund(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_emergency_fund = Depends(account_in_emergency_fund),
# ):
#     return fin_app.update_account_emergency_fund(account_info)
#
# @router.put("/{id}/decimal_places", response_model=account_out)
# def update_decimal_places(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_decimal_places = Depends(account_in_decimal_places),
# ):
#     return fin_app.update_account_decimal_places(account_info)
#
# @router.put("/{id}/archived", response_model=account_out)
# def update_archived(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_archived = Depends(account_in_archived),
# ):
#     return fin_app.update_account_archived(account_info)
#
# @router.put("/{id}/primary", response_model=account_out)
# def update_primary(
#     *,
#     fin_app: Fin_app = Depends(deps.get_fin_service),
#     account_info: account_in_primary = Depends(account_in_primary),
# ):
#     return fin_app.update_account_primary(account_info)
#

@router.get("/archived", response_model=PaginatedResponse)
def get_archived_accounts(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить архивированные счета с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
    """
    accounts = fin_app.get_archived_accounts(skip=skip, limit=limit)
    total_count = fin_app.get_total_archived_accounts()
    has_more = (skip + limit) < total_count
    
    return PaginatedResponse(
        items=accounts,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.get("/primary", response_model=PaginatedResponse)
def get_primary_accounts(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить основные счета с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
    """
    accounts = fin_app.get_primary_accounts(skip=skip, limit=limit)
    total_count = fin_app.get_total_primary_accounts()
    has_more = (skip + limit) < total_count
    
    return PaginatedResponse(
        items=accounts,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.delete("/{id}", response_model=account_out)
def delete_account(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    id:UUID,
):
    """
    Удалить учетную запись.
    
    Параметры:
        id: UUID учетной записи
    """
    return fin_app.delete_account(id)

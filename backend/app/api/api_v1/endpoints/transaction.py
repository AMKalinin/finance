from datetime import date
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Query 
from pydantic import BaseModel

from app.api import deps
from app.schemas.distribution import distribution_settle_in
from app.schemas.position import position_in, position_out
from app.schemas.transaction import (
    distribution_in,
    distribution_out,
    transaction_in,
    transaction_in_date,
    transaction_in_description,
    transaction_in_size,
    transaction_out,
)
from app.service.fin_app import Fin_app
from app.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


class PaginatedTransactionsResponse(BaseModel):
    """Ответ с пагинацией для транзакций."""
    items: List[transaction_out]
    total: int
    skip: int
    limit: int
    has_more: bool = False


@router.get("/all", response_model=PaginatedTransactionsResponse)
def get_all(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить все транзакции с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей (макс. 1000)
    """
    logger.info(f"Получение списка транзакций с пагинацией", extra={"skip": skip, "limit": limit})
    
    transactions = fin_app.get_all_transaction(skip=skip, limit=limit)
    total_count = fin_app.get_total_transactions()
    has_more = (skip + limit) < total_count
    
    return PaginatedTransactionsResponse(
        items=transactions,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )


@router.get("/by_period", response_model=PaginatedTransactionsResponse)
def get_all_by_period(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    from_date: date,
    to_date: date,
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить транзакции за период с пагинацией.
    
    Параметры:
        from_date: Дата начала (YYYY-MM-DD)
        to_date: Дата окончания (YYYY-MM-DD)
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
    """
    transactions = fin_app.get_all_transaction_for_period(
        from_date, to_date, skip=skip, limit=limit
    )
    total_count = fin_app.get_total_transactions_for_period(from_date, to_date)
    has_more = (skip + limit) < total_count
    
    return PaginatedTransactionsResponse(
        items=transactions,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.get("/by_period_type", response_model=PaginatedTransactionsResponse)
def get_all_by_period_with_type(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    from_date: date,
    to_date: date,
    operation_type: str,
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить транзакции за период с фильтрацией по типу и пагинацией.
    
    Параметры:
        from_date: Дата начала (YYYY-MM-DD)
        to_date: Дата окончания (YYYY-MM-DD)
        operation_type: Тип операции (debit, adding, transfer)
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
    """
    transactions = fin_app.get_all_transaction_for_period_with_type(
        from_date, to_date, operation_type, skip=skip, limit=limit
    )
    total_count = fin_app.get_total_transactions_for_period_with_type(
        from_date, to_date, operation_type
    )
    has_more = (skip + limit) < total_count
    
    return PaginatedTransactionsResponse(
        items=transactions,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )


@router.post("/create", response_model=transaction_out)
def create_transaction(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), transaction_info: transaction_in
):
    return fin_app.create_transaction(transaction_info)


@router.post("/distribution", response_model=distribution_out)
def add_distribution(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), distribution_info: distribution_in
):
    return fin_app.transaction_add_distribution(distribution_info)


@router.patch("/distribution", response_model=distribution_out)
def update_distribution(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), distribution_info: distribution_in
):
    return fin_app.transaction_update_distribution(distribution_info)


@router.delete("/distribution", response_model=distribution_out)
def delete_distribution(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), distribution_info: distribution_in
):
    return fin_app.transaction_delete_distribution(distribution_info)


@router.patch("/distribution/settle", response_model=distribution_out)
def settle_distribution(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), settle_info: distribution_settle_in
):
    """Пометить распределение как оплаченное."""
    return fin_app.transaction_settle_distribution(settle_info)


@router.get("/{transaction_id}/distributions", response_model=List[distribution_out])
def get_distributions(
    *,
    transaction_id: UUID,
    fin_app: Fin_app = Depends(deps.get_fin_service),
):
    """Получить все распределения транзакции."""
    return fin_app.get_transaction_distributions(transaction_id)


@router.post("/position", response_model=position_out)
def add_position(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), position_info: position_in
):
    return fin_app.transaction_add_position(position_info)


@router.patch("/position", response_model=position_out)
def update_position(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), position_info: position_in
):
    return fin_app.transaction_update_position(position_info)


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


@router.put("/{id}", response_model=transaction_out)
def update_transaction(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    id: UUID,
    transaction_info: transaction_in,
):
    """Полное обновление транзакции."""
    return fin_app.update_transaction(id, transaction_info)


@router.delete("/{id}", response_model=transaction_out)
def delete_transaction(*, fin_app: Fin_app = Depends(deps.get_fin_service), id: UUID):
    return fin_app.delete_transaction(id)

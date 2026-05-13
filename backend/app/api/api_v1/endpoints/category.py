from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.api import deps
from app.schemas.category import category_in, category_in_name, category_out
from app.service.fin_app import Fin_app
from app.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


class PaginatedCategoriesResponse(BaseModel):
    """Ответ с пагинацией для категорий."""
    items: List[category_out]
    total: int
    skip: int
    limit: int
    has_more: bool = False


@router.get("/", response_model=PaginatedCategoriesResponse)
def get_all_category(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить все категории с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей (макс. 1000)
    """
    logger.info(f"Получение списка категорий с пагинацией", extra={"skip": skip, "limit": limit})
    
    categories = fin_app.get_all_category_structured_list(skip=skip, limit=limit)
    total_count = fin_app.get_total_categories()
    has_more = (skip + limit) < total_count
    
    return PaginatedCategoriesResponse(
        items=categories,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )


@router.post("/create", response_model=category_out)
def create_category(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), category_info: category_in
):
    return fin_app.create_category(category_info)


@router.put("/{id}/name", response_model=category_out)
def update_name(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    category_info: category_in_name = Depends(category_in_name),
):
    return fin_app.update_category(category_info)


@router.get("/type/expenses", response_model=PaginatedCategoriesResponse)
def get_expense_categories(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить категории расходов с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
    """
    categories = fin_app.get_expense_categories(skip=skip, limit=limit)
    total_count = fin_app.get_total_expense_categories()
    has_more = (skip + limit) < total_count
    
    return PaginatedCategoriesResponse(
        items=categories,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.get("/type/income", response_model=PaginatedCategoriesResponse)
def get_income_categories(
    fin_app: Fin_app = Depends(deps.get_fin_service),
    skip: int = Query(0, ge=0, alias="skip"),
    limit: int = Query(100, ge=1, le=1000, alias="limit")
):
    """
    Получить категории доходов с пагинацией.
    
    Параметры:
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
    """
    categories = fin_app.get_income_categories(skip=skip, limit=limit)
    total_count = fin_app.get_total_income_categories()
    has_more = (skip + limit) < total_count
    
    return PaginatedCategoriesResponse(
        items=categories,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.delete("/{id}")
def delete_category(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    id: UUID
):
    """
    Удалить категорию.
    
    Параметры:
        id: UUID категории
    """
    return fin_app.delete_category(id) 

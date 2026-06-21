from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.api import deps
from app.schemas.category import category_in, category_in_name, CategorySchema
from app.service.fin_app import Fin_app
from app.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

def serialize_category_with_children(category):
    """Рекурсивно сериализует категорию со всеми вложенными детьми."""
    if category is None:
        return None
    
    result = {
        'id': str(category.id),
        'name': category.name,
        'type': category.type,
        'level': category.level,
        'children': []  # subCategory alias будет добавлен автоматически
    }
    
    if hasattr(category, 'children') and category.children:
        result['children'] = [serialize_category_with_children(child) for child in category.children]
    
    return result


class PaginatedCategoriesResponse(BaseModel):
    """Ответ с пагинацией для категорий."""
    items: List[dict]  # Сериализованные категории со вложенными детьми
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
    
    # Сериализуем категории с детьми
    serialized_items = [serialize_category_with_children(cat) for cat in categories]

    return PaginatedCategoriesResponse(
        items=serialized_items,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.post("/create", response_model=dict)
def create_category(
    *, fin_app: Fin_app = Depends(deps.get_fin_service), category_info: category_in
):
    """Создать новую категорию."""
    result = fin_app.create_category(category_info)
    return serialize_category_with_children(result)

@router.put("/{id}/name", response_model=dict)
def update_name(
    *,
    fin_app: Fin_app = Depends(deps.get_fin_service),
    category_info: category_in_name = Depends(category_in_name),
):
    """Обновить название категории."""
    result = fin_app.update_category(category_info)
    return serialize_category_with_children(result)

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
    
    serialized_items = [serialize_category_with_children(cat) for cat in categories]

    return PaginatedCategoriesResponse(
        items=serialized_items,
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
    
    serialized_items = [serialize_category_with_children(cat) for cat in categories]

    return PaginatedCategoriesResponse(
        items=serialized_items,
        total=total_count,
        skip=skip,
        limit=limit,
        has_more=has_more
    )

@router.delete("/{id}", response_model=dict)
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
    result = fin_app.delete_category(id)
    return serialize_category_with_children(result)

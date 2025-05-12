from fastapi import APIRouter, Depends

from app.api import deps
from app.schemas.category import category_in, category_in_name, category_out
from app.service.fin_app import Fin_app

router = APIRouter()


@router.get("/", response_model=list[category_out])
def get_all_category(fin_app: Fin_app = Depends(deps.get_fin_service)):
    return fin_app.get_all_category()


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


@router.delete("/{category_id}")
def delete_category(test: str):
    return {test}

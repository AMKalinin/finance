from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.category import category_in, category_in_name, category_out

router = APIRouter()


@router.get("/", response_model=list[category_out])
def get_all_category(db: Session = Depends(deps.get_db)):
    return crud.category.get_all(db)


@router.post("/create", response_model=category_out)
def create_category(*, db: Session = Depends(deps.get_db), category_info: category_in):
    return crud.category.create_category(db, category_info)


@router.put("/{id}/name", response_model=category_out)
def update_name(
    *,
    db: Session = Depends(deps.get_db),
    category_info: category_in_name = Depends(category_in_name),
):
    return crud.category.update_name(db, category_info)


@router.delete("/{category_id}")
def delete_category(test: str):
    return {test}

from fastapi import APIRouter, Depends

from app.api import deps

router = APIRouter()


@router.get("/test")
def get_all_category(user = Depends(deps.get_fin_service)):
    return user

from fastapi import APIRouter

router = APIRouter()


@router.post("/create")
def create_category(test: str):
    return {test}


@router.delete("/{category_id}")
def delete_category(test: str):
    return {test}

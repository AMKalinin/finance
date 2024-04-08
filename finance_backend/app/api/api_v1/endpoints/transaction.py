from fastapi import APIRouter

router = APIRouter()


@router.post("/create")
def create_transaction(test: str):
    return {test}


@router.delete("/{transaction_id}")
def delete_transaction(test: str):
    return {test}

from fastapi import APIRouter

router = APIRouter()


@router.get("/{account_id}/balance")
def get_account_balance(test: str):
    return {test}


@router.post("/create")
def create_account(test: str):
    return {test}


@router.delete("/{account_id}")
def delete_account(test: str):
    return {test}

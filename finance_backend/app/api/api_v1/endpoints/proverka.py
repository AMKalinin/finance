from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_test(test: str):
    return {test}

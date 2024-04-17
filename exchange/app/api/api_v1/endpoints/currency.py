from fastapi import APIRouter

# from sqlalchemy.orm import Session

# from app.api import deps

router = APIRouter()


@router.get("/")
def get_currency() -> dict[tuple[str, str], int]:
    return {("usd", "rub"): 94}

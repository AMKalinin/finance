from fastapi import APIRouter

from app.api.api_v1.endpoints import currency
from app.api.api_v1.endpoints import exchange

api_router = APIRouter()

api_router.include_router(currency.router, prefix="/currency", tags=["currency"])

api_router.include_router(exchange.router, prefix="/exchange", tags=["exchange"])

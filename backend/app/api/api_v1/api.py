from fastapi import APIRouter

from app.api.api_v1.endpoints import account, category, transaction

api_router = APIRouter()

api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(transaction.router, prefix="/transaction", tags=["transaction"])

from fastapi import APIRouter

from app.api.api_v1.endpoints import payment

api_router = APIRouter()

api_router.include_router(payment.router, prefix="/payment", tags=["payment"])

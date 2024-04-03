from fastapi import APIRouter

from app.api.api_v1.endpoints import proverka

api_router = APIRouter()

api_router.include_router(proverka.router, prefix="/test")
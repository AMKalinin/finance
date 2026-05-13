import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.err.handlers import setup_exception_handlers, logger
from app.logging_config import RequestLoggingMiddleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_fastapi_app():
    app = FastAPI(
        title="Finance API",
        description="REST API для управления личными финансами",
        version=settings.VERSION,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )
    app.include_router(api_router, prefix=settings.API_V1_STR)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )
    
    # Регистрация обработчиков ошибок
    setup_exception_handlers(app)
    
    # Middleware для логирования HTTP запросов (в разработке)
    if settings.DEBUG:
        app.add_middleware(RequestLoggingMiddleware)
    
    return app


init_db()

app = create_fastapi_app()


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint для проверки работоспособности API.
    Используется для мониторинга и health checks.
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "api": f"{settings.API_V1_STR}"
    }


@app.get("/", tags=["Root"])
async def root():
    """
    Главная страница API.
    Перенаправляет на документацию Swagger UI.
    """
    return {
        "message": "Welcome to Finance API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc"
    }

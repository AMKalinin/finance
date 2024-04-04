from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

# import uvicorn

# import sys


def create_fastapi_app():
    app = FastAPI(title="Finance API", openapi_url="/openapi.json")
    app.include_router(api_router, prefix=settings.API_V1_STR)
    # adsad
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
    return app


app = create_fastapi_app()


class A:
    x = 2

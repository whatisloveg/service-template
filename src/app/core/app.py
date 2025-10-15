from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.broker.router import router
from app.broker import handlers

def create_app() -> FastAPI:
    app = FastAPI(title="Lead manager API",
                  version="1.0.0")
    app.include_router(api_router, prefix="/api/v1")

    app.include_router(router)
    return app
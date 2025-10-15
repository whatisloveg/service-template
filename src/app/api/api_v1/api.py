from fastapi import APIRouter
from app.api.api_v1.endpoints.health import router as health_router



api_router = APIRouter()
api_router.include_router(health_router)
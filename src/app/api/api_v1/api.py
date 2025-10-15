from fastapi import APIRouter
from app.api.api_v1.endpoints.heath_example import router as health_router



api_router = APIRouter()
api_router.include_router(health_router)
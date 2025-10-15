from fastapi import APIRouter
from app.core.logger import logger


router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health_check():
    """Проверяет здоровье сервера"""
    try:
        return "ok"
    except Exception as e:
        logger.error(f" error {e} ")
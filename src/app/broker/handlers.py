"""Файл где реализуются хандлеры сообщений из очередей"""
import asyncio
from aiohttp import TCPConnector
from fastapi import Depends
from app.core.logger import logger
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession
from app.broker.dependencies import get_broker
from app.broker.router import router
from app.core.settings import config
from app.schemas.broker.messages import *
from app.db.async_session import get_session
import aiohttp

@router.subscriber(config.queues_cfg.NAME1, response_model=TemplateMessageResponse)
async def handle_template(
        msg: TemplateMessageRequest,
        db: AsyncSession = Depends(get_session),
):
    logger.info(f"Сообщение :{msg}")
    try:
        #любая логика
        return TemplateMessageResponse(success=True)
    except Exception as e:
        logger.error(f"Ошибка {msg.id}, error {e} ")
        return TemplateMessageResponse(success=False)

from typing import Annotated

from faststream import Depends
from faststream.rabbit import RabbitQueue

from app.broker.router import router
from app.core.logger import logger
from app.core.settings import config
from app.db.async_session import get_session
from app.schemas.broker.messages import TemplateMessageRequest, TemplateMessageResponse
from sqlalchemy.ext.asyncio import AsyncSession


@router.subscriber(RabbitQueue(config.queues_cfg.NAME1, durable=True))
async def handle_template(
    msg: TemplateMessageRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TemplateMessageResponse:
    logger.info("Сообщение получено | id=%s", msg.id)

    # любая логика

    return TemplateMessageResponse(success=True)

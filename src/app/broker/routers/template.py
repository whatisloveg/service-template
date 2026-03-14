from typing import Annotated

from faststream import Depends
from faststream.rabbit import RabbitQueue, RabbitRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.dependencies import get_db_session
from app.core.logger import logger
from app.core.settings import config
from app.schemas.broker.messages import TemplateMessageRequest, TemplateMessageResponse

template_router = RabbitRouter()


@template_router.subscriber(RabbitQueue(config.queues_cfg.NAME1, durable=True))
async def handle_template(
    data: TemplateMessageRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TemplateMessageResponse:
    logger.info("Сообщение получено | data=%s", data)

    # любая логика

    return TemplateMessageResponse(success=True)

from typing import Annotated

from faststream import Depends
from faststream.rabbit import RabbitQueue, RabbitRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.dependencies import get_db_session
from app.core.logger import logger
from app.core.settings import config
from app.repository.template_repository import TemplateRepository
from app.schemas.broker.messages import TemplateMessageRequest, TemplateMessageResponse
from app.services.template_service import TemplateService

template_router = RabbitRouter()


def _build_service(session: AsyncSession) -> TemplateService:
    """Собирает TemplateService из broker-зависимостей."""
    return TemplateService(
        session=session,
        template_repo=TemplateRepository(session=session),
    )


@template_router.subscriber(RabbitQueue(config.queues_cfg.NAME1, durable=True))
async def handle_template(
    data: TemplateMessageRequest,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TemplateMessageResponse:
    logger.info("Сообщение получено | data=%s", data)

    service = _build_service(session)
    return await service.handle(data)

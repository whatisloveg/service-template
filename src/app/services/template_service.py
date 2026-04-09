from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.template_repository import TemplateRepository
from app.schemas.broker.messages import TemplateMessageRequest, TemplateMessageResponse


class TemplateService:
    def __init__(self, session: AsyncSession, template_repo: TemplateRepository) -> None:
        self.session = session
        self.template_repo = template_repo

    async def handle(self, data: TemplateMessageRequest) -> TemplateMessageResponse:
        # TODO: добавить бизнес-логику
        return TemplateMessageResponse(success=True)

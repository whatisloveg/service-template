from sqlalchemy.ext.asyncio import AsyncSession


class TemplateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # TODO: добавить методы работы с БД

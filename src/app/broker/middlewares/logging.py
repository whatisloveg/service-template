from types import TracebackType

from faststream import BaseMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseMiddleware):
    async def on_receive(self) -> None:
        routing_key = getattr(self.msg, "routing_key", None) or "unknown"
        logger.info("Входящее сообщение из очереди %s", routing_key)

    async def after_processed(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> bool | None:
        if exc_type is None:
            logger.info("Сообщение обработано успешно")
        else:
            logger.error(
                "Ошибка при обработке сообщения | %s: %s",
                exc_type.__name__,
                exc_val,
            )
        return await super().after_processed(exc_type, exc_val, exc_tb)

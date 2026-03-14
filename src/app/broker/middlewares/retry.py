from types import TracebackType

from faststream import BaseMiddleware
from faststream.exceptions import NackMessage, RejectMessage

from app.core.logger import logger
from app.core.settings import config

RETRYABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
    ConnectionError,
    TimeoutError,
    OSError,
)


class RetryMiddleware(BaseMiddleware):
    def _get_retry_count(self) -> int:
        raw = getattr(self.msg, "raw_message", None)
        if raw and getattr(raw, "headers", None):
            return int(raw.headers.get("x-retry", 0))
        return 0

    async def after_processed(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> bool | None:
        if exc_type is None:
            return await super().after_processed(exc_type, exc_val, exc_tb)

        if issubclass(exc_type, RETRYABLE_EXCEPTIONS):
            retry_count = self._get_retry_count()
            max_retry = config.rabbitmq_cfg.MAX_RETRY_COUNT
            if retry_count < max_retry:
                logger.warning(
                    "Transient ошибка, retry №%d/%d: %s: %s",
                    retry_count + 1,
                    max_retry,
                    exc_type.__name__,
                    exc_val,
                )
                raise NackMessage() from exc_val

            logger.error(
                "Лимит retry (%d) исчерпан, сообщение отклоняется: %s",
                max_retry,
                exc_val,
            )
            raise RejectMessage() from exc_val

        logger.error(
            "Фатальная ошибка при обработке, сообщение отклоняется: %s: %s",
            exc_type.__name__,
            exc_val,
        )
        raise RejectMessage() from exc_val

"""
Middleware для логирования сообщений.

Извлекает X-Trace-ID из headers (проставляется gateway).
При отсутствии header — генерирует новый UUID.
"""

import uuid
from typing import Any

from faststream import BaseMiddleware
from faststream.message import StreamMessage

from app.core.logger import logger, request_id_var


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware для установки контекста логирования.

    Использует consume_scope для доступа к распарсенному StreamMessage,
    который содержит headers из RabbitMQ-сообщения.
    """

    async def consume_scope(
        self,
        call_next: Any,
        msg: "StreamMessage",
    ) -> Any:
        """Оборачивает обработку сообщения, устанавливая контекст логирования."""
        try:
            headers = getattr(msg, "headers", {}) or {}
            trace_id = headers.get("X-Trace-ID") or str(uuid.uuid4())[:12]
            request_id_token = request_id_var.set(trace_id)

            routing_key = getattr(msg, "path", None) or getattr(self.msg, "routing_key", None) or "unknown"
            logger.info("Входящее сообщение из очереди %s", routing_key)

        except Exception as e:
            logger.error("Ошибка в LoggingMiddleware: %s", e, exc_info=True)
            request_id_token = request_id_var.set(str(uuid.uuid4())[:12])

        try:
            result = await call_next(msg)
            logger.info("Сообщение обработано успешно")
            return result
        except Exception as exc:
            logger.error(
                "Ошибка при обработке сообщения | %s: %s",
                type(exc).__name__,
                exc,
            )
            raise
        finally:
            request_id_var.reset(request_id_token)

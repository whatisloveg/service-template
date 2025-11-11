import logging
import sys
from contextvars import ContextVar
from typing import Optional
import logging_loki
from app.core.settings import config

# ContextVars для отслеживания контекста запросов
request_id_var: ContextVar[str] = ContextVar("request_id", default="unknown")
user_id_var: ContextVar[str] = ContextVar("user_id", default="unknown")


class ContextFilter(logging.Filter):
    """Добавляет request_id и user_id в каждую запись лога"""

    def filter(self, record):
        record.request_id = request_id_var.get()
        record.user_id = user_id_var.get()
        return True


def setup_logging(
        service_name: Optional[str] = None,
        environment: Optional[str] = None,
        log_level: Optional[str] = None,
        loki_url: Optional[str] = None,
):
    """
    Настраивает логирование один раз при старте приложения.

    Логика:
    - develop: только консольный вывод
    - production: консоль + Loki
    """
    # Используем значения из конфига по умолчанию
    service_name = service_name or config.app_cfg.SERVICE_NAME
    environment = environment or config.app_cfg.ENVIRONMENT
    log_level = log_level or config.logging_cfg.LOG_LEVEL
    loki_url = loki_url or config.logging_cfg.LOKI_URL

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.handlers.clear()

    context_filter = ContextFilter()

    # Console Handler - всегда активен
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    console_formatter = logging.Formatter(
        "[%(request_id)s] [%(user_id)s] %(asctime)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(context_filter)
    logger.addHandler(console_handler)

    # Loki Handler - только для production
    if environment == "production":
        try:
            loki_handler = logging_loki.LokiHandler(
                url=loki_url,
                tags={
                    "service": service_name,
                    "environment": environment,
                },
                version="1",
            )
            loki_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
            loki_formatter = logging.Formatter(
                "%(request_id)s | %(user_id)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s"
            )
            loki_handler.setFormatter(loki_formatter)
            loki_handler.addFilter(context_filter)
            logger.addHandler(loki_handler)
            logging.info("✅ Loki handler configured: %s", loki_url)
        except Exception as e:
            logging.warning("❌ Failed to configure Loki handler: %s", e)

    logging.info(
        "✅ Logging configured | Service: %s | Environment: %s | Level: %s | Loki: %s",
        service_name,
        environment,
        log_level,
        "enabled" if environment == "production" else "disabled"
    )


logger = logging.getLogger(__name__)
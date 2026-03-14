from faststream.rabbit.fastapi import RabbitRouter

from app.broker.middlewares.logging import LoggingMiddleware
from app.broker.middlewares.retry import RetryMiddleware
from app.broker.routers.template import template_router
from app.core.logger import logger
from app.core.settings import config

router = RabbitRouter(
    url=config.rabbitmq_cfg.url,
    logger=logger,
    middlewares=[
        RetryMiddleware,
        LoggingMiddleware,
    ],
)

router.include_router(template_router)
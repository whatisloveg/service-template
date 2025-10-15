from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.broker.router import router
from app.broker import handlers
from app.core.logger import logger
from app.core.settings import config


def create_app() -> FastAPI:
    app = FastAPI(title="Lead manager API",
                  version="1.0.0")
    app.include_router(api_router, prefix="/api/v1")

    if config.rabbitmq_cfg.is_configured:

        app.include_router(router)
        logger.info("RabbitMQ router included")
    else:
        logger.warning("RabbitMQ disabled, broker router skipped")

    return app
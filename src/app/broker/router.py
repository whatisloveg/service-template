from faststream.rabbit.fastapi import RabbitRouter
from app.core.settings import config
from app.core.logger import logger

router = RabbitRouter(config.rabbitmq_cfg.url,
                      logger=logger)
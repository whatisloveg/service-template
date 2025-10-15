from faststream.rabbit import RabbitBroker
from app.broker.router import router


def get_broker() -> RabbitBroker:
    """Dependency для получения RabbitBroker в REST endpoints"""
    return router.broker
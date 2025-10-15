from typing import Optional, Any
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator, ValidationInfo
from dotenv import load_dotenv

load_dotenv()


class AppConfig(BaseSettings):
    """Общие настройки приложения"""
    SERVICE_NAME: str = "notify-service"
    ENVIRONMENT: str = "production"
    TZ: str = "Europe/Moscow"

    class Config:
        env_prefix = ""


class LoggingConfig(BaseSettings):
    """Конфигурация логирования"""
    LOG_LEVEL: str = "INFO"
    LOKI_URL: str = "http://loki:3100/loki/api/v1/push"
    LOKI_ENABLED: bool = True

    class Config:
        env_prefix = ""


class DBConfig(BaseSettings):
    """Конфигурация PostgreSQL"""
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str
    PORT: int = 5432

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("USER"),
            password=values.data.get("PASSWORD"),
            host=values.data.get("HOST"),
            port=values.data.get("PORT"),
            path=f"{values.data.get('DATABASE')}",
        )

    @property
    def sqlalchemy_async_database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    @property
    def sqlalchemy_sync_database_uri(self) -> str:
        """URL для синхронных операций (миграции)"""
        return f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"

    class Config:
        env_prefix = "DB_"


class RabbitMQConfig(BaseSettings):
    ENABLED: bool = True
    USER: str
    PASS: str
    HOST: str
    PORT: int = 5672

    @property
    def url(self) -> str:
        """Собирает AMQP URL из компонентов"""
        return f"amqp://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/"

    @property
    def is_configured(self) -> bool:
        """Проверка, настроен ли RabbitMQ"""
        return self.ENABLED and bool(self.USER and self.PASS and self.HOST)

    class Config:
        env_prefix = "RABBITMQ_"


class QueuesConfig(BaseSettings):
    NAME1: str
    NAME2: str

    class Config:
        env_prefix = "QUEUE_"


class RedisConfig(BaseSettings):
    """Конфигурация Redis"""
    HOST: Optional[str] = None
    PORT: Optional[int] = None

    @field_validator("HOST", "PORT", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        """Преобразует пустые строки в None"""
        if v == "" or v is None:
            return None
        return v

    @property
    def url(self) -> Optional[str]:
        if self.HOST and self.PORT:
            return f"redis://{self.HOST}:{self.PORT}"
        return None

    @property
    def is_configured(self) -> bool:
        """Проверка, настроен ли Redis"""
        return bool(self.HOST and self.PORT)

    class Config:
        env_prefix = "REDIS_"

class Settings(BaseSettings):
    """Контейнер всех настроек приложения"""
    app_cfg: AppConfig = AppConfig()
    logging_cfg: LoggingConfig = LoggingConfig()
    db_cfg: DBConfig = DBConfig()
    rabbitmq_cfg: RabbitMQConfig = RabbitMQConfig()
    queues_cfg: QueuesConfig = QueuesConfig()
    redis_cfg: RedisConfig = RedisConfig()


config = Settings()
from typing import Optional, Any
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator, ValidationInfo
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()


class DBConfig(BaseSettings):
    """
    Конфигурация PostgreSQL
    """
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
    USER: str
    PASS: str
    HOST: str
    PORT: int = 5672

    @property
    def url(self) -> str:
        """Собирает AMQP URL из компонентов"""
        return f"amqp://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/"

    class Config:
        env_prefix = "RABBITMQ_"


class QueuesConfig(BaseSettings):
    NAME1: str
    NAME2: str

    class Config:
        env_prefix = "QUEUE_"


class Settings(BaseSettings):
    """
    Контейнер всех настроек приложения
    """
    db_cfg: DBConfig = DBConfig()
    rabbitmq_cfg: RabbitMQConfig = RabbitMQConfig()
    queues_cfg: QueuesConfig = QueuesConfig()

config = Settings()
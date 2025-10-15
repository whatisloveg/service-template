import asyncio
import subprocess
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.settings import config
from app.core.logger import logger


async def wait_for_db(max_attempts: int = 3, delay: int = 2):
    """Ждём пока БД станет доступна"""
    engine = create_async_engine(
        config.db_cfg.sqlalchemy_async_database_uri,
        echo=False
    )

    for attempt in range(max_attempts):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Database is ready!")
            await engine.dispose()
            return
        except Exception as e:
            logger.warning(f"Database not ready, retrying... {max_attempts - attempt} attempts left. Error: {e}")
            await asyncio.sleep(delay)

    await engine.dispose()
    raise Exception("Could not connect to database")


async def run_migrations():
    """Запуск миграций через subprocess"""
    logger.info("Starting migrations...")

    try:
        # Запускаем alembic как отдельный процесс
        process = await asyncio.create_subprocess_exec(
            "alembic", "upgrade", "head",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info(f"Migrations completed! Output: {stdout.decode()}")
        else:
            logger.error(f"Migration failed! Error: {stderr.decode()}")
            raise Exception("Migration failed")

    except Exception as e:
        logger.error(f"Migration error: {e}")
        raise
from starlette.middleware.cors import CORSMiddleware
from app.core.app import create_app
import app.models
from app.core.logger import setup_logging
from app.core.logger import logger
from app.db import migrations

setup_logging(service_name="notify-service", environment="production")

app =  create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    logger.info("Starting application...")
    await migrations.wait_for_db()
    logger.info("DB check completed, starting migrations...")
    await migrations.run_migrations()
    logger.info("All startup tasks completed!")
    pass


@app.on_event("shutdown")
async def shutdown() -> None:
    pass
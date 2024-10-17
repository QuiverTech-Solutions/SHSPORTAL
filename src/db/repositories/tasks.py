"""Database Connect Tasks"""

import logging

from databases import Database
from fastapi import FastAPI

from src.core.config import DATABASE_URL

app_logger = logging.getLogger("app")


async def connect_database(app: FastAPI) -> None:
    """Connect to DB"""
    try:
        database = Database(DATABASE_URL)
        await database.connect()
        app.state._db = database
        app_logger.info("Connected to postgres db.")
    except Exception as e:
        app_logger.exception("Failed to connect to postgresql db", exc_info=e)


async def disconnect_database(app: FastAPI) -> None:
    """Close db."""
    try:
        await app.state._db.disconnect()
        app_logger.info("Disconnected from postgresql db")
    except Exception as e:
        app_logger.exception("Error disconnecting from postgresql", exc_info=e)

"""Core task: Connect and Disconnect to db when application starts and stops."""

from typing import Callable

from fastapi import FastAPI

from src.db.repositories.tasks import connect_database, disconnect_database


def create_start_app_handler(app: FastAPI) -> Callable:
    """Connect to db."""

    async def start_app() -> None:
        await connect_database(app)
        print("Application started")
        print("Application started")

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Disconnect db."""

    async def stop_app() -> None:
        await disconnect_database(app)
        print("Application stopped")
        print("Application stopped")

    return stop_app

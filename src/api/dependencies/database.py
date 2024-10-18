"""Dependency for db."""

# Standard library imports
import asyncio
import logging
from typing import Any, Callable, Dict, Type, Union

from databases import Database

# Third party imports
from fastapi import Depends
from starlette.requests import Request

from src.db.repositories.base import BaseRepository

app_logger = logging.getLogger("app")


def get_database(request: Request) -> Database:
    """Get Postgresql database from app state."""
    return request.app.state._db


def get_repository(repo_type: Union[Type[BaseRepository], BaseRepository]) -> Callable:
    """Dependency for db."""

    def get_repo(
        db: Database = Depends(get_database),
    ) -> Type[BaseRepository]:
        return repo_type(db)  # type: ignore

    return get_repo

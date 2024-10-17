"""Crud routers."""

from fastapi import APIRouter

crud_router = APIRouter()


@crud_router.get("/")
async def read_root() -> dict:
    """Read the root."""
    return {"Hello": "World"}

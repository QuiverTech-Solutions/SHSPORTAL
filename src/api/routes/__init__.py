"""Route configuration for the application."""

from fastapi import FastAPI


def setup_routes(app: FastAPI) -> None:
    """Configure all application routes."""
    from src.api.routes.crud_router import crud_router
    from src.api.routes.paystack import paystack_router
    from src.api.routes.schools import school_router

    app.include_router(crud_router, prefix="/crud", tags=["CRUD"])
    app.include_router(school_router, prefix="/schools", tags=["Schools"])
    app.include_router(paystack_router, prefix="/paystack", tags=["Paystack"])

    @app.get("/", name="index")
    async def index() -> str:
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."

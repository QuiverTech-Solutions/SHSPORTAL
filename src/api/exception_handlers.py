"""Exception handlers for the application."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.errors.core import CoreError
from src.errors.paystack import PaystackError


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure all exception handlers."""

    @app.exception_handler(PaystackError)
    async def paystack_exception_handler(
        request: Request, exc: PaystackError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

    @app.exception_handler(CoreError)
    async def database_exception_handler(
        request: Request, exc: CoreError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"detail": exc.message}
        )

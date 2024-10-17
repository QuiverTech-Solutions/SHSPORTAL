"""Middleware configuration for the application."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.core.config import SECRET_KEY

request_logger = logging.getLogger("request")


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware."""
    origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next: callable) -> JSONResponse:
        client_ip = request.client.host
        method = request.method
        path = request.url.path
        request_logger.info(f"Incoming request: {method} {path} from {client_ip}")

        response = await call_next(request)

        status_code = response.status_code
        request_logger.info(f"Response: {status_code}")

        return response

    # app.add_middleware(APIKeyMiddleware)


class APIKeyMiddleware:
    """API key middleware."""

    async def __call__(self, request: Request, call_next: callable) -> JSONResponse:
        """Check if the API key is valid."""
        if request.method == "OPTIONS":
            return await call_next(request)

        api_key = request.headers.get("x-api-key")
        if api_key != SECRET_KEY:
            return JSONResponse(status_code=403, content={"detail": "Invalid API Key"})
        return await call_next(request)

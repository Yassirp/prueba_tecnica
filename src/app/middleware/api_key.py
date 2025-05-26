from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.app.shared.constants.settings import Settings
from src.app.shared.utils.request_utils import http_response
from fastapi import status

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Rutas que no requieren API key
        public_paths = ["/", "/docs", "/redoc", "/openapi.json", "/favicon.ico"]
        
        if (
            request.url.path in public_paths
            or request.url.path.startswith("/static")
        ):
            return await call_next(request)
        
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return http_response(
                message="API key is missing",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if api_key != Settings.APP_KEY:
            return http_response(
                message="Invalid API key",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return await call_next(request)
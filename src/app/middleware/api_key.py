from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..shared.constants.settings import Settings

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip API key check for docs and openapi
        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
            
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise HTTPException(status_code=401, detail="API Key is missing")
        if api_key != Settings.API_KEY:
            raise HTTPException(status_code=403, detail="Invalid API Key")
        return await call_next(request) 
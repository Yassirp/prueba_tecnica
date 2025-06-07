import base64
import json
import pytz
from typing import Callable, Awaitable
from fastapi import Request, Response
from src.app.config.database.session import SessionLocal
from src.app.modules.access_tokens_module.services.access_tokens_service import AccessTokenService
from starlette.middleware.base import BaseHTTPMiddleware
from src.app.shared.constants.settings import Settings
from src.app.shared.utils.request_utils import http_response
from fastapi import status
from datetime import datetime
from fastapi import HTTPException

class APIKeyMiddleware(BaseHTTPMiddleware):
    excluded_paths = {
        "/auth/login",
        "/docs",
        "/redoc", 
        "/openapi.json", 
        "/favicon.ico",
        "/"
    }
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            # Excluir rutas específicas
            if request.url.path in self.excluded_paths:
                return await call_next(request)
            
            auth_header = request.headers.get("Authorization")
            
            if auth_header:
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
                    if token: 
                        async with SessionLocal() as session:
                            access_token_service = AccessTokenService(session)
                            data, count = await access_token_service.get_all(token=token, limit=1)                        
                            if not count:
                                raise Exception("El token es inválido.")
                            
                            for value in data:
                                if datetime.now(pytz.timezone("America/Bogota")) >= value.expires_at:
                                    # Eliminar el token
                                    await session.delete(value)
                                    await session.commit()
                                    raise Exception("El token es inválido.")

                            decoded_bytes = base64.b64decode(token)
                            decoded_str = decoded_bytes.decode('utf-8')
                            query_params = json.loads(decoded_str)  # dict resultante
                            request.state.query_params = query_params  # por ejemplo, un dict con user_id, region_id, etc.
                else:
                    raise Exception("Authorization header presente pero no es Bearer")
            else:
                raise Exception("Error de autenticacion.")

            return await call_next(request)
        except Exception as e:
            return http_response(
                message="Middleware de autenticacion",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=[],
                errors=[f"{str(e)}"]
            )


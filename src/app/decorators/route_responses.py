from functools import wraps
from fastapi import status, HTTPException
from typing import Callable, Any, Optional, TypeVar, cast
from src.app.shared.utils.request_utils import http_response
from src.app.shared.constants.messages import GlobalMessages

T = TypeVar("T")

def handle_route_responses(
    success_message: str, error_message: str, not_found_message: Optional[str] = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await func(*args, **kwargs)

                # Handle not found cases
                if result is None or (isinstance(result, tuple) and result[0] is None):
                    return http_response(
                        message=not_found_message or GlobalMessages.ERROR_NOT_FOUND,
                        status=status.HTTP_404_NOT_FOUND,
                    )

                return http_response(
                    message=success_message, data=result, status=status.HTTP_200_OK
                )
            except HTTPException as http_ex:
                return http_response(
                    message=error_message,
                    errors=[str(http_ex.detail)],
                    status=http_ex.status_code,
                )
            except Exception as e:
                return http_response(
                    message=error_message,
                    errors=[str(e)],
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return cast(Callable[..., Any], wrapper)

    return decorator

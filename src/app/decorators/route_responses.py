from functools import wraps
from fastapi import status
from typing import Callable, Any
from ..shared.utils.request_utils import http_response
from ..shared.constants.messages import GlobalMessages

def handle_route_responses(success_message: str, error_message: str, not_found_message: str = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                result = await func(*args, **kwargs)
    
                # Handle not found cases
                if (result is None or (isinstance(result, tuple) and result[0] is None)):
                    return http_response(
                        message=not_found_message or GlobalMessages.ERROR_NOT_FOUND,
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                return http_response(
                    message=success_message,
                    data=result,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return http_response(
                    message=error_message,
                    errors=[str(e)],
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return wrapper
    return decorator
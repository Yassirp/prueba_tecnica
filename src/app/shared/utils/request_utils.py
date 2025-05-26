from fastapi.responses import JSONResponse
from typing import Any, Dict, List, Optional, Callable, TypeVar, Sequence, Union
from pydantic import ValidationError
from fastapi.encoders import jsonable_encoder

T = TypeVar("T")

def paginated_response(
    items: Sequence[T],
    total: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    serialize_fn: Optional[Callable[[T], Any]] = None,
) -> Dict[str, Any]:
    response = {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [serialize_fn(item) for item in items] if serialize_fn else items,
    }
    return response


def get_errors_validations(e: ValidationError) -> List[Dict[str, str]]:
    errors: List[Dict[str, str]] = []
    for error in e.errors():
        loc = error["loc"]
        if loc[0] == "body" and len(loc) > 1:
            field = str(loc[1])
        else:
            field = str(loc[0])
        message = str(error["msg"])
        errors.append({"field": field, "message": message})
    return errors


def http_response(
    message: str,
    data: Optional[Dict[str, Any]] = None,
    errors: Optional[List[Union[str, Dict[str, str]]]] = None,
    status: int = 200,
) -> JSONResponse:
    response_data = {"message": message, "status": status, "status_ok": status < 400}

    if data is not None:
        response_data["data"] = jsonable_encoder(data)

    if errors is not None:
        response_data["errors"] = errors

    return JSONResponse(content=response_data, status_code=status)

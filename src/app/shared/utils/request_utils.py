from fastapi.responses import JSONResponse
from typing import Any, Dict, List, Optional 
    
def paginated_response(items, total, limit=None, offset=None, serialize_fn=lambda x: x):
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [serialize_fn(item) for item in items] if serialize_fn else items
    }
    
def get_errors_validations(e: any):
    errors = []
    for error in e.errors():
        loc = error['loc']
        if loc[0] == 'body' and len(loc) > 1:
            field = loc[1]
        else:
            field = loc[0]
        message = error['msg']
        errors.append({
            "field": field,
            "message": message
        })
    return errors

def http_response(
    message: str, 
    data: Optional[Dict[str, Any]] = None,
    errors: Optional[List[Any]] = None, 
    status: int = 200
) -> JSONResponse:
    response_data = {
        "message": message,
        "status": status,
        "status_ok": status < 400
    }
    
    if data is not None:
        response_data["data"] = data
        
    if errors is not None:
        response_data["errors"] = errors
        
    return JSONResponse(
        content=response_data,
        status_code=status
    )

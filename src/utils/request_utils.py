from flask import request, jsonify

def get_pagination_params():
    try:
        limit = request.args.get("limit", type=int)
        offset = request.args.get("offset", type=int)
        order_by = request.args.get("order_by", type=str)
        return limit, offset, order_by
    except Exception:
        raise Exception("Invalid pagination parameters")
    
    
def paginated_response(items, total, limit=None, offset=None, serialize_fn=lambda x: x):
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [serialize_fn(item) for item in items] if serialize_fn else items
    }
    
def get_filter_params():
    skip = {"limit", "offset", "order_by"}
    return {
        key: value
        for key, value in request.args.items()
        if key not in skip and value is not None
    }
    
def get_errors_validations(e: any):
    errors = []
    for error in e.errors():
        field = error['loc'][0]
        message = error['msg']
        errors.append({
            "field": field,
            "message": message
        })
    return errors


def http_response(message: str, data: dict = {}, errors: list = [], status: int = 200):
    return jsonify({
        "message": message,
        "errors": errors,
        "data": data,
        "status": status
    }), status

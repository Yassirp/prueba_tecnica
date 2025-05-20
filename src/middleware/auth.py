from functools import wraps
from flask import jsonify
from .fake_auth import set_current_user

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            set_current_user()
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated
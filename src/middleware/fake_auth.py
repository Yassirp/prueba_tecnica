from flask import request
import jwt
from utils.constants import Settings
def set_fake_user():
    class FakeUser:
        def __init__(self):
            self.id = 2
            self.old_id = 1

    request.user = FakeUser()
    
    
def set_current_user():
    if Settings.DEBUG:
        set_fake_user()
        return
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Authorization token missing or malformed")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
        class AuthenticatedUser:
            def __init__(self, data):
                self.id = data.get("id")
                self.old_id = data.get("role_id")
        request.user = AuthenticatedUser(payload)
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
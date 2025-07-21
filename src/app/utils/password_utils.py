import random
import string
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    @staticmethod
    def hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def generate(length: int = 10) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
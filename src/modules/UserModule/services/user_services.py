from services.base_services import BaseService
from sqlalchemy.orm import Session
from modules.UserModule.repositories.user_repository import UserRepository
from modules.UserModule.models.users import User
from modules.UserModule.schemas.user_schema import UserCreateSchema, UserUpdateSchema

class UserService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
        super().__init__(User, self.repository, UserCreateSchema, UserUpdateSchema)

from sqlalchemy.orm import Session
from modules.UserModule.models.users import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = User
        super().__init__(self.db, self.model)
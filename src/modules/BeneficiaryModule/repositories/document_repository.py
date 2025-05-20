from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from modules.BeneficiaryModule.models.documents import Document



class  DocumentRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        self.model = Document
        super().__init__(self.db, self.model)


    def get_by_associate_and_document_types(self, document_types:list[int], associate_to: str, associate_id: int):
        return (self.db.query(self.model)
            .filter(self.model.document_type.in_(document_types))
            .filter(self.model.associate_to == associate_to)
            .filter(self.model.associate_id == associate_id)
            .filter(self.model.deleted_at.is_(None))
            .all())


from sqlalchemy.ext.asyncio import AsyncSession
from src.app.shared.bases.base_service import BaseService
from src.app.modules.document_module.models.documents import Document
from src.app.modules.document_module.repositories.document_repository import DocumentRepository
from src.app.modules.document_module.schemas.document_schemas import DocumentOut
from src.app.modules.document_module.services.s3_service import S3Service
from fastapi import UploadFile
from uuid import uuid4
from fastapi import HTTPException
from src.app.modules.parameters_module.models.parameters_values import ParameterValue
from src.app.modules.parameters_module.repositories.parameter_values_repository import ParameterValueRepository

class DocumentService(BaseService[Document, DocumentOut]):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repository = DocumentRepository(Document, self.db_session)
        self.parameter_value_repository = ParameterValueRepository(ParameterValue, self.db_session)
        super().__init__(
            model=Document,
            repository_cls=DocumentRepository,
            db_session=self.db_session,
            out_schema=DocumentOut,
        )
        
    async def create_and_upload(self, data: dict, file: UploadFile):
        try:
            type = await self.parameter_value_repository.get_by_id(data["document_type"])
            if not type:
                raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
            
            # 1. Subir el archivo a S3
            value_type = str(type.reference) if type.reference is not None else str(type.value)
            
            filename = f"{value_type}/{uuid4()}_{file.filename}"
            s3_url = await S3Service.upload_file(file=file, filename=filename)

            # 2. Completar la data
            data["path"] = filename
            data["url"] = s3_url

            # 3. Crear documento en la base de datos
            document = await self.repository.create(data)
            await self.db_session.refresh(document, ['type', 'user'])
            # 4. Retornar el esquema
            return self._serialize_model(document)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
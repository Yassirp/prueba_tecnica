from fastapi import APIRouter, Depends, status, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from typing import Optional
from src.app.modules.document_module.schemas.document_schemas import DocumentOut, DocumentCreate, DocumentUpdate
from src.app.modules.document_module.services.document_service import DocumentService
from src.app.shared.utils.request_utils import paginated_response, http_response
from src.app.middleware.api_auth import require_auth, User 

router = APIRouter(prefix="/document", tags=["Document"])



@router.get("/{document_id}", response_model=DocumentOut, status_code=status.HTTP_200_OK)
async def get_document(document_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_auth)):
    document = await DocumentService(db).get_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return http_response(message="Documento obtenido correctamente", data=document)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_document(data: DocumentCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_auth)):
    document = await DocumentService(db).create(data.model_dump())
    return http_response(message="Documento creado correctamente", data=document)


@router.put("/{document_id}", status_code=status.HTTP_200_OK)
async def update_document(document_id: int, data: DocumentUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_auth)):
    document = await DocumentService(db).update(document_id, data.model_dump())
    return http_response(message="Documento actualizado correctamente", data=document)

@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_auth)):
    await DocumentService(db).delete(document_id)
    return http_response(message="Documento eliminado correctamente")


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_documents(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_auth)):
    documents, total = await DocumentService(db).get_all(limit=10,offset=0, order_by="id:asc", filters={"active": True})
    paginate_ =  paginated_response(documents,total,limit=10,offset=0)
    return http_response(message="Documentos obtenidos correctamente", data=paginate_)


@router.post("/create-and-upload", status_code=status.HTTP_200_OK)
async def create_and_upload_document(
    associate_id: Optional[int] = Form(None),
    associate_to: Optional[str] = Form(None),
    document_type: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    data = {
        "associate_id": associate_id,
        "associate_to": associate_to,
        "document_type": document_type,
        "description": description,
        "created_by": current_user.id,
    }

    document = await DocumentService(db).create_and_upload(data, file)
    return http_response(message="Documento creado correctamente", data=document)

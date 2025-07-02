from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.config.database.session import get_db
from src.app.modules.user_module.schemas.users_schemas import AccessTokenOut, CodeVerification, ValidateLogin, UserCreate, UserOut, UserUpdate
from src.app.modules.user_module.services.user_service import UserService
from src.app.shared.utils.request_utils import paginated_response, http_response
from src.app.middleware.api_auth import require_auth, User 


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/login", response_model=AccessTokenOut, status_code=status.HTTP_200_OK)
async def login(
    data: ValidateLogin, db: AsyncSession = Depends(get_db),
) -> AccessTokenOut:
    service = UserService(db)
    return await service.login(data.model_dump())



@router.get("/all", status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)):
    service = UserService(db)
    register, total= await service.get_all(limit=10,offset=0, order_by="id:asc", filters={"state": 1})
    paginate_ =  paginated_response(register,total,limit=10,offset=0)
    return http_response(message="Usuarios obtenidos correctamente", data=paginate_)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_auth)):
    service = UserService(db)
    user = await service.get_by_id(user_id)
    
    return http_response(message="Usuario obtenido correctamente", data=user)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: dict, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.register(data)


@router.post("/verify", response_model=dict)
async def verify_code(data: CodeVerification, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.verify_user_code(data)


@router.post("/create", response_model=dict)
async def create_user(
    data: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    service = UserService(db)
    return await service.create_user(data)


@router.put("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_auth)
):
    service = UserService(db)
    updated_user = await service.update(user_id, data.model_dump(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user
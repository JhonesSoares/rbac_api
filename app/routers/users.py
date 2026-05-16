from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import hash_password, require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="[Admin] Criar novo usuário",
    description="**Requer perfil Admin.** Cria um novo usuário no sistema.",
)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    current=Depends(require_admin),
):
    # Check email uniqueness
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado.",
        )

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    await db.flush()  # Gera o ID no banco de dados
    await db.refresh(user)  # Atualiza o objeto Python com os dados do banco
    return UserResponse.model_validate(user)

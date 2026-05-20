from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, hash_password, require_admin
from app.models.user import User
from app.schemas.user import MessageResponse, UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.post(
    "/add",
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


@router.get(
    "/list_users",
    response_model=List[UserResponse],
    summary="[Admin] Listar todos os usuários",
    description="**Requer perfil Admin.** Retorna a lista completa de usuários.",
)
async def list_users(
    db: AsyncSession = Depends(get_db),
    current=Depends(require_admin),
):
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/user/{user_id}",
    response_model=UserResponse,
    summary="Buscar usuário por ID",
    description="Admin pode ver qualquer usuário. Usuário comum só pode ver seus próprios dados.",
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(get_current_user),
):
    current_user, _ = current

    # Common users can only see themselves
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Você só pode visualizar seus próprios dados.",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    return UserResponse.model_validate(user)


@router.patch(
    "/user_update/{user_id}",
    response_model=UserResponse,
    summary="[Admin] Atualizar usuário",
    description="**Requer perfil Admin.** Atualiza dados de um usuário existente.",
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current=Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )
    # Campos que não foram enviados são deixados de fora (exclude_unset=True)
    update_data = payload.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_exists = await db.execute(
            select(User).where(User.email == update_data["email"], User.id != user_id)
        )
        if email_exists.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email já em uso."
            )
    # adiciona valores ao obj(user) = setattr(objeto, "nome_do_atributo", valor)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return UserResponse.model_validate(user)


@router.delete(
    "/deactivate_user/{user_id}",
    response_model=MessageResponse,
    summary="[Admin] Desativar usuário 'delete'.",
    description="**Requer perfil Admin.** Desativa (soft delete via is_active=False) um usuário.",
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current=Depends(require_admin),
):
    admin_user, _ = current

    if admin_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode remover sua própria conta.",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    user.is_active = False
    await db.flush()
    return MessageResponse(message=f"Usuário {user.email} desativado com sucesso.")

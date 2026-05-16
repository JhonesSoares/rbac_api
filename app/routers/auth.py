from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    blacklist_token,
    create_access_token,
    get_current_user,
    verify_password,
)
from app.models.user import User
from app.schemas.user import LoginRequest, MessageResponse, TokenResponse, UserResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticação de usuário",
    description="Autentica o usuário com email e senha, retornando um token JWT.",
)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada. Contate o administrador.",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout do usuário",
    description="Invalida o token JWT atual adicionando-o à blacklist.",
)
async def logout(current=Depends(get_current_user)):
    _, token = current
    blacklist_token(token)
    return MessageResponse(message="Logout realizado com sucesso.")


@router.get(
    "/my_data",
    response_model=UserResponse,
    summary="Dados do usuário atual",
    description="Retorna os dados do usuário autenticado.",
)
async def me(current=Depends(get_current_user)):
    user, _ = current
    return UserResponse.model_validate(user)


@router.get(
    "/refresh_token",
    response_model=TokenResponse,
    summary="Atualiza Token",
    description="Retorna um novo Token do usuário autenticado.",
)
async def refresh_token(current=Depends(get_current_user)):
    user, _ = current
    new_token = create_access_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token=new_token,
        user=UserResponse.model_validate(user),
    )

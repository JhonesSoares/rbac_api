from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserResponse

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

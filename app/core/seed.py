"""
Script para criar o primeiro usuário administrador.
Execute: python -m app.core.seed
"""

import asyncio

from app.models.user import User
from sqlalchemy import select

from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import hash_password


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == settings.FIRST_ADMIN_EMAIL)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"Admin '{settings.FIRST_ADMIN_EMAIL}' já existe. Seed ignorado.")
            return

        admin = User(
            name=settings.FIRST_ADMIN_NAME,
            email=settings.FIRST_ADMIN_EMAIL,
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        await db.commit()
        print(
            f"✅ Admin criado: {settings.FIRST_ADMIN_EMAIL} / {settings.FIRST_ADMIN_PASSWORD}"
        )


if __name__ == "__main__":
    asyncio.run(seed())

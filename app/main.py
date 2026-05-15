from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they don't exist (handled by Alembic in prod)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="User Management API with RBAC",
    description="""
## API de Gerenciamento de Usuários com Role-Based Access Control (RBAC)

### Perfis de Acesso
- **Admin**: Pode criar, listar e visualizar todos os usuários.
- **User**: Pode apenas fazer login/logout e visualizar seus próprios dados.

### Autenticação
Use o endpoint `/auth/login` para obter um token JWT e inclua-o no header:
`Authorization: Bearer <token>`
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, users


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
- **User**: Pode apenas fazer api/v1/login/logout e visualizar seus próprios dados.

### Autenticação
Use o endpoint `/api/v1/auth/login` para obter um token JWT e inclua-o no header:
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
api_version = "/api/v1"
app.include_router(auth.router, prefix=f"{api_version}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{api_version}/users", tags=["Users"])

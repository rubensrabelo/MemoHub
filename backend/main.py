from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

# 1. Configuração do Driver Assíncrono (asyncpg)
postgres_url = ""

# Usamos create_async_engine em vez de create_engine
async_engine = create_async_engine(postgres_url, echo=True)


# 2. Modelo de Dados (Continua igual)
class SystemConfig(SQLModel, table=True):
    __tablename__: str = "system_config"

    id: int | None = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str


# 3. Inicialização Assíncrona do Banco (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Para criar as tabelas de forma assíncrona na inicialização
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(title="MemoHub - Async API", lifespan=lifespan)


# 4. Dependency Injection para as rotas (Garante que a sessão fecha após o uso)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


# 5. Exemplo de Rota Async usando a Session assíncrona
@app.get("/configs")
async def get_configs(session: AsyncSession = Depends(get_session)):
    # Em queries assíncronas do SQLModel, usamos session.exec() precedido de AWAIT
    statement = select(SystemConfig)
    result = await session.exec(statement)
    configs = result.all()
    return configs


@app.get("/health")
def check_health():
    return {"status": "healthy", "message": "Async engine configured via asyncpg"}

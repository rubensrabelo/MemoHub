from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

# Importações da nossa estrutura infra/db
from .infra.db import engine, create_db_and_tables, get_session


# Mantido aqui temporariamente até criarmos a pasta modules/
class SystemConfig(SQLModel, table=True):
    __tablename__: str = "system_config"

    id: int | None = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Chama a função importada para criar as tabelas
    await create_db_and_tables(engine)
    yield


app = FastAPI(title="MemoHub - Modular Monolith Architecture", lifespan=lifespan)


@app.get("/configs")
async def get_configs(session: AsyncSession = Depends(get_session)):
    statement = select(SystemConfig)
    result = await session.exec(statement)
    configs = result.all()
    return configs


@app.get("/health")
def check_health():
    return {"status": "healthy", "message": "Clean architecture structure initialized"}

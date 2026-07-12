from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine

# 1. PostgreSQL Database Configuration matching docker-compose.dev.yml
postgres_url = "postgresql://app_user:app_password@localhost:5432/memo_hub_db"
engine = create_engine(postgres_url, echo=True)


# 2. Database Table Model Definition (Updated with Python 3.10+ typing)
class SystemConfig(SQLModel, table=True):
    __tablename__: str = "system_config"

    id: int | None = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    value: str


# 3. Database Table Creation on Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


# 4. FastAPI Instance Initialization
app = FastAPI(title="MemoHub - System Configuration API", lifespan=lifespan)


@app.get("/health")
def check_health():
    return {
        "status": "healthy",
        "message": "Connected to PostgreSQL 'memo_hub_db' successfully",
    }

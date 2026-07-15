from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infra.db import engine, create_db_and_tables
from .modules import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables(engine)
    yield


app = FastAPI(
    title="MemoHub - Modular Monolith Architecture", lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)
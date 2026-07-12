import logging
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import DATABASE_URL

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)
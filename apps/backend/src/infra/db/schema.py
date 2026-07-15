from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine


async def create_db_and_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
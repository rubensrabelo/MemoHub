from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from fastapi import HTTPException, status
from src.modules.knowledge.models import Knowledge
from src.modules.knowledge.dtos import KnowledgeCreateDTO, KnowledgeUpdateDTO

class KnowledgeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, search: str | None = None, category: str | None = None, favorite: bool | None = None):
        statement = select(Knowledge)
        
        if search:
            statement = statement.where(
                (Knowledge.question.ilike(f"%{search}%")) | 
                (Knowledge.answer.ilike(f"%{search}%"))
            )
            
        if category:
            statement = statement.where(Knowledge.category == category)
            
        if favorite is not None:
            statement = statement.where(Knowledge.favorite == favorite)
            
        statement = statement.order_by(Knowledge.created_at.desc())
        result = await self.db.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, id: int):
        db_knowledge = await self.db.get(Knowledge, id)
        if not db_knowledge:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
        return db_knowledge

    async def create(self, payload: KnowledgeCreateDTO):
        now = datetime.now(timezone.utc)
        data = payload.model_dump()
        data.update({"created_at": now, "updated_at": now})
        
        db_knowledge = Knowledge.model_validate(data)
        self.db.add(db_knowledge)
        await self.db.commit()
        await self.db.refresh(db_knowledge)
        return db_knowledge

    async def update(self, id: int, payload: KnowledgeUpdateDTO):
        db_knowledge = await self.get_by_id(id)
        
        original_created_at = db_knowledge.created_at
        
        data_to_update = payload.model_dump(exclude_unset=True)
        for key, value in data_to_update.items():
            setattr(db_knowledge, key, value)
            
        db_knowledge.created_at = original_created_at
        db_knowledge.updated_at = datetime.now(timezone.utc)
        
        self.db.add(db_knowledge)
        await self.db.commit()
        await self.db.refresh(db_knowledge)
        return db_knowledge

    async def toggle_favorite(self, id: int):
        db_knowledge = await self.get_by_id(id)
        
        original_created_at = db_knowledge.created_at
        
        db_knowledge.favorite = not db_knowledge.favorite
        db_knowledge.created_at = original_created_at
        db_knowledge.updated_at = datetime.now(timezone.utc)
            
        self.db.add(db_knowledge)
        await self.db.commit()
        await self.db.refresh(db_knowledge)
        return db_knowledge

    async def delete(self, id: int):
        db_knowledge = await self.get_by_id(id)
        await self.db.delete(db_knowledge)
        await self.db.commit()

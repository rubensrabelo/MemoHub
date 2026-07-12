from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.infra.db import get_session
from src.modules.knowledge.models import Knowledge
from src.modules.knowledge.dtos import KnowledgeCreateDTO, KnowledgeUpdateDTO, KnowledgeResponseDTO

router = APIRouter()


@router.get("/", response_model=list[KnowledgeResponseDTO])
async def get_all(
    search: str | None = None,
    category: str | None = None,
    favorite: bool | None = None,
    db: AsyncSession = Depends(get_session)
):
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
    result = await db.execute(statement)
    return result.scalars().all()


@router.get("/{id}", response_model=KnowledgeResponseDTO)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)):
    db_knowledge = await db.get(Knowledge, id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return db_knowledge


@router.post("/", response_model=KnowledgeResponseDTO, status_code=status.HTTP_201_CREATED)
async def create(payload: KnowledgeCreateDTO, db: AsyncSession = Depends(get_session)):
    now = datetime.now(timezone.utc)
    data = payload.model_dump()
    data.update({"created_at": now, "updated_at": now})
    
    db_knowledge = Knowledge.model_validate(data)
    db.add(db_knowledge)
    await db.commit()
    await db.refresh(db_knowledge)
    return db_knowledge


@router.put("/{id}", response_model=KnowledgeResponseDTO)
async def update(id: int, payload: KnowledgeUpdateDTO, db: AsyncSession = Depends(get_session)):
    db_knowledge = await db.get(Knowledge, id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    original_created_at = db_knowledge.created_at
    
    data_to_update = payload.model_dump(exclude_unset=True)
    for key, value in data_to_update.items():
        setattr(db_knowledge, key, value)
        
    db_knowledge.created_at = original_created_at
    db_knowledge.updated_at = datetime.now(timezone.utc)
    
    db.add(db_knowledge)
    await db.commit()
    await db.refresh(db_knowledge)
    return db_knowledge


@router.patch("/{id}/favorite", response_model=KnowledgeResponseDTO)
async def toggle_favorite(id: int, db: AsyncSession = Depends(get_session)):
    db_knowledge = await db.get(Knowledge, id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    original_created_at = db_knowledge.created_at
    
    db_knowledge.favorite = not db_knowledge.favorite
    db_knowledge.created_at = original_created_at
    db_knowledge.updated_at = datetime.now(timezone.utc)
        
    db.add(db_knowledge)
    await db.commit()
    await db.refresh(db_knowledge)
    return db_knowledge


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session)):
    db_knowledge = await db.get(Knowledge, id)
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    await db.delete(db_knowledge)
    await db.commit()

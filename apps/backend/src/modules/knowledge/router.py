from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.db import get_session
from src.modules.knowledge.dtos import KnowledgeCreateDTO, KnowledgeUpdateDTO, KnowledgeResponseDTO
from src.modules.knowledge.service import KnowledgeService

router = APIRouter()


@router.get("/", response_model=list[KnowledgeResponseDTO])
async def get_all(
    search: str | None = None,
    category: str | None = None,
    favorite: bool | None = None,
    db: AsyncSession = Depends(get_session)
):
    service = KnowledgeService(db)
    return await service.get_all(search, category, favorite)


@router.get("/{id}", response_model=KnowledgeResponseDTO)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)):
    service = KnowledgeService(db)
    return await service.get_by_id(id)


@router.post("/", response_model=KnowledgeResponseDTO, status_code=status.HTTP_201_CREATED)
async def create(payload: KnowledgeCreateDTO, db: AsyncSession = Depends(get_session)):
    service = KnowledgeService(db)
    return await service.create(payload)


@router.put("/{id}", response_model=KnowledgeResponseDTO)
async def update(id: int, payload: KnowledgeUpdateDTO, db: AsyncSession = Depends(get_session)):
    service = KnowledgeService(db)
    return await service.update(id, payload)


@router.patch("/{id}/favorite", response_model=KnowledgeResponseDTO)
async def toggle_favorite(id: int, db: AsyncSession = Depends(get_session)):
    service = KnowledgeService(db)
    return await service.toggle_favorite(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session)):
    service = KnowledgeService(db)
    await service.delete(id)

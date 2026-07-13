import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.modules.knowledge.service import KnowledgeService
from src.modules.knowledge.dtos import KnowledgeCreateDTO, KnowledgeUpdateDTO
from src.modules.knowledge.models import Knowledge

pytestmark = pytest.mark.asyncio


async def test_unit_service_get_all_success():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    mock_knowledge_list = [
        Knowledge(id=1, question="Q1", answer="A1", category="C1", favorite=False),
        Knowledge(id=2, question="Q2", answer="A2", category="C2", favorite=True)
    ]
    
    mock_scalars.all.return_value = mock_knowledge_list
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result
    
    service = KnowledgeService(mock_db)
    result = await service.get_all(search="teste", category="TI", favorite=True)
    
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].favorite is True
    mock_db.execute.assert_awaited_once()


async def test_unit_service_get_by_id_success():
    mock_db = AsyncMock()
    mock_knowledge = Knowledge(id=3, question="Q3", answer="A3", category="C3", favorite=False)
    mock_db.get.return_value = mock_knowledge
    
    service = KnowledgeService(mock_db)
    result = await service.get_by_id(id=3)
    
    assert result.id == 3
    assert result.question == "Q3"
    mock_db.get.assert_awaited_once_with(Knowledge, 3)


async def test_unit_service_get_by_id_not_found():
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    service = KnowledgeService(mock_db)
    with pytest.raises(HTTPException) as exc_info:
        await service.get_by_id(id=999)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Registro não encontrado"


async def test_unit_service_create_success():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    payload = KnowledgeCreateDTO(
        question="Nova Pergunta",
        answer="Nova Resposta",
        category="Geral",
        favorite=False
    )
    
    service = KnowledgeService(mock_db)
    result = await service.create(payload=payload)
    
    assert result.question == "Nova Pergunta"
    assert isinstance(result.created_at, datetime)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


async def test_unit_service_update_success():
    mock_db = AsyncMock()
    mock_knowledge = Knowledge(
        id=3, 
        question="Antiga", 
        answer="Antiga", 
        category="Antiga", 
        favorite=False,
        created_at=datetime.now(timezone.utc)
    )
    mock_db.get.return_value = mock_knowledge
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    payload = KnowledgeUpdateDTO(
        question="Modificada",
        answer="Modificada",
        category="Modificada",
        favorite=True
    )
    
    service = KnowledgeService(mock_db)
    result = await service.update(id=3, payload=payload)
    
    assert result.question == "Modificada"
    assert result.favorite is True
    mock_db.get.assert_awaited_once_with(Knowledge, 3)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


async def test_unit_service_toggle_favorite_success():
    mock_db = AsyncMock()
    mock_knowledge = Knowledge(
        id=3, 
        question="Q", 
        answer="A", 
        category="C", 
        favorite=False,
        created_at=datetime.now(timezone.utc)
    )
    mock_db.get.return_value = mock_knowledge
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    service = KnowledgeService(mock_db)
    result = await service.toggle_favorite(id=3)
    
    assert result.favorite is True
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


async def test_unit_service_delete_success():
    mock_db = AsyncMock()
    mock_knowledge = Knowledge(id=3, question="Q", answer="A", category="C", favorite=False)
    mock_db.get.return_value = mock_knowledge
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()
    
    service = KnowledgeService(mock_db)
    await service.delete(id=3)
    
    mock_db.delete.assert_awaited_once_with(mock_knowledge)
    mock_db.commit.assert_awaited_once()

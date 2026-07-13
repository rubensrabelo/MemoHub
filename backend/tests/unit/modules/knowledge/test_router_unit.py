import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.modules.knowledge.router import get_all, get_by_id, create, update, toggle_favorite, delete
from src.modules.knowledge.dtos import KnowledgeCreateDTO, KnowledgeUpdateDTO
from src.modules.knowledge.models import Knowledge

pytestmark = pytest.mark.asyncio


async def test_unit_get_all_success():
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    mock_knowledge_list = [
        Knowledge(id=1, question="P1", answer="R1", category="C1", favorite=False),
        Knowledge(id=2, question="P2", answer="R2", category="C2", favorite=True)
    ]
    
    mock_scalars.all.return_value = mock_knowledge_list
    mock_result.scalars.return_value = mock_scalars
    mock_db.execute.return_value = mock_result
    
    result = await get_all(search="teste", category="TI", favorite=True, db=mock_db)
    
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].favorite is True
    mock_db.execute.assert_awaited_once()


async def test_unit_get_by_id_success():
    mock_db = AsyncMock()
    mock_knowledge = Knowledge(id=3, question="P3", answer="R3", category="C3", favorite=False)
    mock_db.get.return_value = mock_knowledge
    
    result = await get_by_id(id=3, db=mock_db)
    
    assert result.id == 3
    assert result.question == "P3"
    mock_db.get.assert_awaited_once_with(Knowledge, 3)


async def test_unit_get_by_id_not_found():
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await get_by_id(id=999, db=mock_db)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Registro não encontrado"


async def test_unit_create_success():
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
    
    result = await create(payload=payload, db=mock_db)
    
    assert result.question == "Nova Pergunta"
    assert isinstance(result.created_at, datetime)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


async def test_unit_update_success():
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
    
    result = await update(id=3, payload=payload, db=mock_db)
    
    assert result.question == "Modificada"
    assert result.favorite is True
    mock_db.get.assert_awaited_once_with(Knowledge, 3)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


async def test_unit_update_not_found():
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    payload = KnowledgeUpdateDTO(question="Q", answer="A", category="C", favorite=False)
    
    with pytest.raises(HTTPException) as exc_info:
        await update(id=999, payload=payload, db=mock_db)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


async def test_unit_toggle_favorite_success():
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
    
    result = await toggle_favorite(id=3, db=mock_db)
    
    assert result.favorite is True
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


async def test_unit_toggle_favorite_not_found():
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await toggle_favorite(id=999, db=mock_db)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


async def test_unit_delete_success():
    mock_db = AsyncMock()
    mock_knowledge = Knowledge(id=3, question="Q", answer="A", category="C", favorite=False)
    mock_db.get.return_value = mock_knowledge
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()
    
    await delete(id=3, db=mock_db)
    
    mock_db.delete.assert_awaited_once_with(mock_knowledge)
    mock_db.commit.assert_awaited_once()


async def test_unit_delete_not_found():
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await delete(id=999, db=mock_db)
        
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

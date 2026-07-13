import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio


async def test_integration_create_and_get_by_id(client):
    payload = {
        "question": "O que faz o depende_on no compose?",
        "answer": "Define a ordem de inicialização de serviços.",
        "category": "Docker",
        "favorite": False
    }
    
    post_res = await client.post("/api/v1/knowledge/", json=payload)
    assert post_res.status_code == status.HTTP_201_CREATED
    
    created_data = post_res.json()
    knowledge_id = created_data["id"]
    
    get_res = await client.get(f"/api/v1/knowledge/{knowledge_id}")
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["question"] == payload["question"]


async def test_integration_get_all_with_filters(client):
    p1 = {"question": "Erro CORS Vue", "answer": "Liberar middleware", "category": "Frontend", "favorite": True}
    p2 = {"question": "Alembic setup", "answer": "Executar revision", "category": "Database", "favorite": False}
    
    await client.post("/api/v1/knowledge/", json=p1)
    await client.post("/api/v1/knowledge/", json=p2)
    
    res_search = await client.get("/api/v1/knowledge/?search=CORS")
    assert len(res_search.json()) == 1
    assert res_search.json()[0]["category"] == "Frontend"
    
    res_fav = await client.get("/api/v1/knowledge/?favorite=true")
    assert len(res_fav.json()) == 1
    assert res_fav.json()[0]["question"] == "Erro CORS Vue"


async def test_integration_update_success(client):
    payload = {"question": "Q Antiga", "answer": "A Antiga", "category": "Geral", "favorite": False}
    post_res = await client.post("/api/v1/knowledge/", json=payload)
    knowledge_id = post_res.json()["id"]
    
    update_payload = {"question": "Q Nova", "answer": "A Nova", "category": "Geral", "favorite": True}
    put_res = await client.put(f"/api/v1/knowledge/{knowledge_id}", json=update_payload)
    
    assert put_res.status_code == status.HTTP_200_OK
    assert put_res.json()["question"] == "Q Nova"
    assert put_res.json()["created_at"] == post_res.json()["created_at"]


async def test_integration_toggle_favorite(client):
    payload = {"question": "Q1", "answer": "A1", "category": "Geral", "favorite": False}
    post_res = await client.post("/api/v1/knowledge/", json=payload)
    knowledge_id = post_res.json()["id"]
    
    patch_res = await client.patch(f"/api/v1/knowledge/{knowledge_id}/favorite")
    assert patch_res.status_code == status.HTTP_200_OK
    assert patch_res.json()["favorite"] is True


async def test_integration_delete_success(client):
    payload = {"question": "Deletar", "answer": "Remover", "category": "Geral", "favorite": False}
    post_res = await client.post("/api/v1/knowledge/", json=payload)
    knowledge_id = post_res.json()["id"]
    
    del_res = await client.delete(f"/api/v1/knowledge/{knowledge_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT
    
    get_res = await client.get(f"/api/v1/knowledge/{knowledge_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND

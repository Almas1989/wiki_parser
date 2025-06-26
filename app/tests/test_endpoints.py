import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert "Wikipedia Parser API" in response.json()["message"]


@pytest.mark.asyncio
async def test_parse_endpoint(async_client):
    response = await async_client.post(
        "/api/v1/parse",
        json={"url": "https://ru.wikipedia.org/wiki/Python"}
    )
    assert response.status_code == 200
    assert "Парсинг запущен" in response.json()["message"]


@pytest.mark.asyncio
async def test_summary_not_found(async_client):
    response = await async_client.get(
        "/api/v1/summary?url=https://ru.wikipedia.org/wiki/NonExistentArticle"
    )
    assert response.status_code == 404

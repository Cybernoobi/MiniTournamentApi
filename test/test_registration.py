from datetime import datetime

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Tournament
from main import app


@pytest_asyncio.fixture
async def test_client(db_session: AsyncSession):
    transport = ASGITransport(app=app)
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(transport=transport, base_url=f"http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def setup_tournament(db_session: AsyncSession):
    tournament = Tournament(
        name="Test Cup",
        max_players=1,
        start_at=datetime.fromisoformat("2025-06-01T15:00:00Z")
    )
    async with db_session as session:  # type: AsyncSession
        session.add(tournament)
        await db_session.commit()
        await db_session.refresh(tournament)
        return tournament


@pytest.mark.asyncio
async def test_successful_registration(test_client, setup_tournament):
    response = await test_client.post(
        f"/tournaments/{setup_tournament.id}/register",
        json={"name": "Alice", "email": "alice@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_duplicate_email_registration(test_client, setup_tournament):
    tournament = setup_tournament
    await test_client.post(
        f"/tournaments/{tournament.id}/register",
        json={"name": "Alice", "email": "alice@example.com"}
    )
    response = await test_client.post(
        f"/tournaments/{tournament.id}/register",
        json={"name": "Alice", "email": "alice@example.com"}
    )
    assert response.status_code == 409
    assert "уже зарегистрирован" in response.json()["detail"]


@pytest.mark.asyncio
async def test_tournament_full(test_client, setup_tournament):
    # max_players = 1, уже регистрируем одного
    tournament = setup_tournament
    await test_client.post(
        f"/tournaments/{tournament.id}/register",
        json={"name": "Bob", "email": "bob@example.com"}
    )
    # пробуем второго
    response = await test_client.post(
        f"/tournaments/{tournament.id}/register",
        json={"name": "Charlie", "email": "charlie@example.com"}
    )
    assert response.status_code == 400
    assert "Турнир полон" in response.json()["detail"]

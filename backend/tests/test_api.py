"""
Quantum Chess Ultimate — API Integration Tests

Tests the FastAPI endpoints using httpx.AsyncClient.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.game_manager import GameManager
from app.services.cache_manager import CacheManager
from app.api.websocket import ConnectionManager
from app.api.routes import game as game_routes
from app.api.routes import quantum as quantum_routes
from app.api.routes import analysis as analysis_routes


@pytest_asyncio.fixture
async def client():
    """Create test client with all services initialized."""
    # Manually initialize services (lifespan doesn't run in test transport)
    cache = CacheManager()
    gm = GameManager(cache=cache)
    ws = ConnectionManager()

    app.state.game_manager = gm
    app.state.cache_manager = cache
    app.state.ws_manager = ws

    game_routes.set_game_manager(gm)
    quantum_routes.set_game_manager(gm)
    analysis_routes.set_game_manager(gm)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestRootEndpoints:
    @pytest.mark.asyncio
    async def test_root(self, client):
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "name" in data
        assert "endpoints" in data

    @pytest.mark.asyncio
    async def test_health(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"


class TestGameAPI:
    @pytest.mark.asyncio
    async def test_create_game(self, client):
        resp = await client.post("/api/game/new", json={"mode": "quantum"})
        assert resp.status_code == 200
        data = resp.json()
        assert "game_id" in data
        assert "state" in data

    @pytest.mark.asyncio
    async def test_get_game(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.get(f"/api/game/{game_id}")
        assert resp.status_code == 200
        assert resp.json()["game_id"] == game_id

    @pytest.mark.asyncio
    async def test_get_nonexistent_game(self, client):
        resp = await client.get("/api/game/nonexistent")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_make_move(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.post(
            f"/api/game/{game_id}/move",
            json={"from_square": "e2", "to_square": "e4"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True

    @pytest.mark.asyncio
    async def test_get_legal_moves(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.get(f"/api/game/{game_id}/legal-moves/e2")
        assert resp.status_code == 200
        data = resp.json()
        assert "e3" in data["legal_moves"]
        assert "e4" in data["legal_moves"]

    @pytest.mark.asyncio
    async def test_delete_game(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.delete(f"/api/game/{game_id}")
        assert resp.status_code == 200


class TestQuantumAPI:
    @pytest.mark.asyncio
    async def test_evaluate_position(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.post(f"/api/quantum/{game_id}/evaluate")
        assert resp.status_code == 200
        data = resp.json()
        assert "classical_score" in data
        assert "quantum_score" in data

    @pytest.mark.asyncio
    async def test_get_circuit(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.get(f"/api/quantum/{game_id}/circuit")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_qubits" in data


class TestAnalysisAPI:
    @pytest.mark.asyncio
    async def test_analyze_position(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.post(f"/api/analysis/{game_id}/position")
        assert resp.status_code == 200
        data = resp.json()
        assert "white" in data
        assert "black" in data

    @pytest.mark.asyncio
    async def test_get_history(self, client):
        create = await client.post("/api/game/new", json={})
        game_id = create.json()["game_id"]
        resp = await client.get(f"/api/analysis/{game_id}/history")
        assert resp.status_code == 200
        assert resp.json()["move_count"] == 0

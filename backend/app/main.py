"""
Quantum Chess Ultimate - FastAPI Application

Main entry point for the backend API server.
Configures CORS, routes, WebSocket, and application lifecycle.
"""

import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.services.game_manager import GameManager
from app.services.cache_manager import CacheManager
from app.api.websocket import ConnectionManager, handle_websocket_message
from app.api.routes import game as game_routes
from app.api.routes import quantum as quantum_routes
from app.api.routes import analysis as analysis_routes

# ─── Logging Setup ────────────────────────────────────────────────────────────

settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ─── Application Lifecycle ────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application resources."""
    # Startup
    logger.info("🚀 Starting Quantum Chess Ultimate API")
    cache = CacheManager()
    game_manager = GameManager(cache=cache)
    ws_manager = ConnectionManager()

    app.state.game_manager = game_manager
    app.state.cache_manager = cache
    app.state.ws_manager = ws_manager

    # Inject game manager into route modules
    game_routes.set_game_manager(game_manager)
    quantum_routes.set_game_manager(game_manager)
    analysis_routes.set_game_manager(game_manager)

    logger.info("✅ All services initialized")
    yield

    # Shutdown
    logger.info("🛑 Shutting down Quantum Chess Ultimate API")
    await cache.clear()
    logger.info("✅ Cleanup complete")


# ─── FastAPI App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Quantum Chess with quantum computing integration",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(game_routes.router)
app.include_router(quantum_routes.router)
app.include_router(analysis_routes.router)


# ─── Root & Health Endpoints ──────────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "game": "/api/game",
            "quantum": "/api/quantum",
            "analysis": "/api/analysis",
            "websocket": "/ws/{game_id}",
        },
    }


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/stats", tags=["Health"])
async def stats():
    gm: GameManager = app.state.game_manager
    ws: ConnectionManager = app.state.ws_manager
    return {
        "games": gm.get_stats(),
        "websocket_connections": ws.get_total_connections(),
    }


# ─── WebSocket Endpoint ──────────────────────────────────────────────────────

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for real-time game communication."""
    ws_manager: ConnectionManager = app.state.ws_manager
    game_manager: GameManager = app.state.game_manager

    await ws_manager.connect(game_id, websocket)

    try:
        # Send initial state if game exists
        state = game_manager.get_state(game_id)
        if state:
            await ws_manager.send_personal(websocket, {
                "type": "state_update",
                "data": state.model_dump(mode="json"),
            })
        else:
            await ws_manager.send_personal(websocket, {
                "type": "error",
                "data": {"message": f"Game {game_id} not found"},
            })

        # Message loop
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                await handle_websocket_message(
                    game_id, message, game_manager, ws_manager
                )
            except json.JSONDecodeError:
                await ws_manager.send_personal(websocket, {
                    "type": "error",
                    "data": {"message": "Invalid JSON"},
                })

    except WebSocketDisconnect:
        ws_manager.disconnect(game_id, websocket)
    except Exception as e:
        logger.error(f"WebSocket error for game {game_id}: {e}")
        ws_manager.disconnect(game_id, websocket)

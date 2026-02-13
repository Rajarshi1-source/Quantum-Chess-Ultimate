"""
Quantum Chess Ultimate - Game API Routes

REST endpoints for game management:
- Create, get, delete games
- Make moves, get legal moves
- List active games
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.game import GameConfig, GameState, GameCreateResponse
from app.models.move import Move, MoveResult, LegalMovesResponse

router = APIRouter(prefix="/api/game", tags=["Game"])

# Game manager is injected from main.py via app.state
_game_manager = None


def set_game_manager(gm):
    global _game_manager
    _game_manager = gm


def get_gm():
    if _game_manager is None:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    return _game_manager


@router.post("/new", response_model=GameCreateResponse)
async def create_game(config: Optional[GameConfig] = None):
    """Create a new quantum chess game."""
    gm = get_gm()
    state = gm.create_game(config)
    return GameCreateResponse(game_id=state.game_id, state=state)


@router.get("/{game_id}", response_model=GameState)
async def get_game(game_id: str):
    """Get current game state."""
    gm = get_gm()
    state = gm.get_state(game_id)
    if not state:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return state


@router.post("/{game_id}/move", response_model=MoveResult)
async def make_move(game_id: str, move: Move):
    """Make a move in a game."""
    gm = get_gm()
    result = gm.make_move(game_id, move)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return result


@router.get("/{game_id}/legal-moves/{square}", response_model=LegalMovesResponse)
async def get_legal_moves(game_id: str, square: str):
    """Get legal moves for a piece at a square."""
    gm = get_gm()
    moves = gm.get_legal_moves(game_id, square)
    if moves is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return LegalMovesResponse(square=square, legal_moves=moves)


@router.get("/{game_id}/all-legal-moves")
async def get_all_legal_moves(game_id: str):
    """Get all legal moves for the current player."""
    gm = get_gm()
    moves = gm.get_all_legal_moves(game_id)
    if moves is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return {"game_id": game_id, "moves": moves}


@router.delete("/{game_id}")
async def delete_game(game_id: str):
    """Delete a game."""
    gm = get_gm()
    success = gm.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return {"message": f"Game {game_id} deleted"}


@router.get("/", response_model=list)
async def list_games():
    """List all active games."""
    gm = get_gm()
    return gm.list_games()

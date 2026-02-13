"""
Quantum Chess Ultimate - Analysis API Routes

REST endpoints for position analysis and probability calculations.
"""

from fastapi import APIRouter, HTTPException

from app.core.evaluator import PositionEvaluator

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])

_game_manager = None


def set_game_manager(gm):
    global _game_manager
    _game_manager = gm


def get_gm():
    if _game_manager is None:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    return _game_manager


@router.post("/{game_id}/position")
async def analyze_position(game_id: str):
    """Full position analysis with component breakdown."""
    gm = get_gm()
    game = gm.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    white_eval = PositionEvaluator.evaluate(
        board=game.engine.board,
        superposition_squares=game.engine.superposition_squares,
        entanglement_pairs=game.engine.entanglement_pairs,
        color="white",
    )
    black_eval = PositionEvaluator.evaluate(
        board=game.engine.board,
        superposition_squares=game.engine.superposition_squares,
        entanglement_pairs=game.engine.entanglement_pairs,
        color="black",
    )

    return {
        "game_id": game_id,
        "white": white_eval,
        "black": black_eval,
        "move_count": game.move_count,
        "superposition_count": len(game.engine.superposition_squares),
        "entanglement_count": len(game.engine.entanglement_pairs),
    }


@router.get("/{game_id}/history")
async def get_move_history(game_id: str):
    """Get the move history for a game."""
    gm = get_gm()
    game = gm.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    return {
        "game_id": game_id,
        "move_count": game.move_count,
        "moves": game.move_history,
        "captured_pieces": game.captured_pieces,
    }


@router.get("/{game_id}/probability/{square}")
async def get_square_probability(game_id: str, square: str):
    """Get probability distribution for a specific square."""
    gm = get_gm()
    game = gm.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    piece = game.engine.board.get(square)
    if piece is None:
        return {
            "game_id": game_id,
            "square": square,
            "occupied": False,
            "probability": 0.0,
        }

    return {
        "game_id": game_id,
        "square": square,
        "occupied": True,
        "piece_type": piece["type"],
        "color": piece["color"],
        "in_superposition": piece.get("in_superposition", False),
        "probability": piece.get("probability", 1.0),
    }

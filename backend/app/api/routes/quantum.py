"""
Quantum Chess Ultimate - Quantum API Routes

REST endpoints for quantum operations:
- Evaluate positions
- Trigger measurements
- Get circuit info
- Find best moves
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.models.quantum import (
    QuantumMeasurement, CircuitInfo, SuperpositionState,
    QuantumEvaluation,
)
from app.core.evaluator import PositionEvaluator
from app.services.circuit_optimizer import CircuitOptimizer

router = APIRouter(prefix="/api/quantum", tags=["Quantum"])

_game_manager = None


def set_game_manager(gm):
    global _game_manager
    _game_manager = gm


def get_gm():
    if _game_manager is None:
        raise HTTPException(status_code=500, detail="Game manager not initialized")
    return _game_manager


class MeasureRequest(BaseModel):
    square: Optional[str] = None  # None = measure all


@router.post("/{game_id}/evaluate", response_model=QuantumEvaluation)
async def evaluate_position(game_id: str):
    """Evaluate the quantum position of a game."""
    gm = get_gm()
    game = gm.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    eval_result = PositionEvaluator.evaluate(
        board=game.engine.board,
        superposition_squares=game.engine.superposition_squares,
        entanglement_pairs=game.engine.entanglement_pairs,
        color=game.turn.value,
    )

    return QuantumEvaluation(
        game_id=game_id,
        classical_score=eval_result["classical_score"],
        quantum_score=eval_result["quantum_score"],
        combined_score=eval_result["combined_score"],
        uncertainty=abs(eval_result["quantum_score"]) * 0.1,
        evaluation_depth=game.engine.search_depth,
        samples_taken=game.engine.shots,
    )


@router.get("/{game_id}/best-move")
async def get_best_move(game_id: str):
    """Find the best move using quantum minimax."""
    gm = get_gm()
    result = gm.find_best_move(game_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return {"game_id": game_id, **result}


@router.post("/{game_id}/measure")
async def measure(game_id: str, request: MeasureRequest):
    """Measure quantum state (single square or all)."""
    gm = get_gm()
    if request.square:
        result = gm.measure_square(game_id, request.square)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
        return {"game_id": game_id, "measured": {request.square: result}}
    else:
        results = gm.measure_all(game_id)
        if results is None:
            raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
        return {"game_id": game_id, "measured": results}


@router.get("/{game_id}/circuit")
async def get_circuit_info(game_id: str):
    """Get quantum circuit information for a game."""
    gm = get_gm()
    game = gm.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    circuit_info = game.engine.get_circuit_info()
    analysis = CircuitOptimizer.analyze_circuit(
        circuit_info["superposition_count"],
        circuit_info["entanglement_count"],
    )
    return {"game_id": game_id, **analysis}


@router.get("/{game_id}/superposition")
async def get_superposition_states(game_id: str):
    """Get all superposition states in a game."""
    gm = get_gm()
    game = gm.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

    states = game.engine.get_superposition_states()
    return {"game_id": game_id, "superposition_states": states}

"""
Quantum Chess Ultimate - Quantum Models
Pydantic models for quantum measurements, circuits, and states.
"""

from pydantic import BaseModel, Field
from typing import Optional


class QuantumMeasurement(BaseModel):
    """Result of measuring the quantum board state."""
    game_id: str
    measured_squares: dict[str, dict] = {}
    collapsed_superpositions: list[str] = []
    measurement_count: int = 0
    timestamp: str = ""


class CircuitInfo(BaseModel):
    """Information about the quantum circuit for a game."""
    game_id: str
    total_qubits: int = 0
    circuit_depth: int = 0
    gate_count: int = 0
    superposition_count: int = 0
    entanglement_count: int = 0


class SuperpositionState(BaseModel):
    """Superposition state of a specific square."""
    square: str
    piece_type: str
    color: str
    probability: float = Field(ge=0.0, le=1.0)
    entangled_with: Optional[str] = None


class QuantumEvaluation(BaseModel):
    """Result of quantum position evaluation."""
    game_id: str
    classical_score: float
    quantum_score: float
    combined_score: float
    uncertainty: float
    best_move: Optional[str] = None
    evaluation_depth: int = 0
    samples_taken: int = 0


class ProbabilityDistribution(BaseModel):
    """Probability distribution for a move outcome."""
    move: str
    outcomes: dict[str, float] = {}
    expected_value: float = 0.0
    variance: float = 0.0

"""
Quantum Chess Ultimate - Game Models
Pydantic models for game state, configuration, and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class GameMode(str, Enum):
    """Available game modes."""
    CLASSICAL = "classical"
    QUANTUM = "quantum"
    HYBRID = "hybrid"
    TUTORIAL = "tutorial"


class PieceColor(str, Enum):
    """Chess piece colors."""
    WHITE = "white"
    BLACK = "black"


class PieceType(str, Enum):
    """Chess piece types."""
    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"


class GameStatus(str, Enum):
    """Game status."""
    ACTIVE = "active"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW = "draw"
    RESIGNED = "resigned"


class PieceInfo(BaseModel):
    """Information about a chess piece."""
    type: PieceType
    color: PieceColor
    in_superposition: bool = False
    superposition_probability: float = 1.0


class GameConfig(BaseModel):
    """Configuration for creating a new game."""
    mode: GameMode = GameMode.QUANTUM
    quantum_probability: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Probability of quantum effects triggering"
    )
    search_depth: int = Field(default=3, ge=1, le=6)
    player_white: str = "Player 1"
    player_black: str = "Player 2"


class GameState(BaseModel):
    """Full game state representation."""
    game_id: str
    mode: GameMode
    status: GameStatus = GameStatus.ACTIVE
    turn: PieceColor = PieceColor.WHITE
    position: dict[str, PieceInfo] = {}
    move_count: int = 0
    measurement_count: int = 0
    quantum_probability: float = 0.5
    superposition_squares: list[str] = []
    entanglement_pairs: list[tuple[str, str]] = []
    move_history: list[dict] = []
    captured_pieces: dict[str, list[str]] = {"white": [], "black": []}
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class GameSummary(BaseModel):
    """Lightweight game summary for listings."""
    game_id: str
    mode: GameMode
    status: GameStatus
    turn: PieceColor
    move_count: int
    player_white: str
    player_black: str
    created_at: datetime


class GameCreateResponse(BaseModel):
    """Response when creating a new game."""
    game_id: str
    state: GameState
    message: str = "Game created successfully"

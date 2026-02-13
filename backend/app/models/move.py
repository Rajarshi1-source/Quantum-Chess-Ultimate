"""
Quantum Chess Ultimate - Move Models
Pydantic models for chess moves and move results.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Move(BaseModel):
    """A chess move request."""
    from_square: str = Field(
        ..., pattern=r"^[a-h][1-8]$",
        description="Source square in algebraic notation (e.g., 'e2')"
    )
    to_square: str = Field(
        ..., pattern=r"^[a-h][1-8]$",
        description="Target square in algebraic notation (e.g., 'e4')"
    )
    promotion: Optional[str] = Field(
        default=None,
        description="Promotion piece type if pawn reaches last rank"
    )


class MoveResult(BaseModel):
    """Result of executing a move."""
    success: bool
    from_square: str
    to_square: str
    piece_moved: str
    piece_captured: Optional[str] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_stalemate: bool = False
    quantum_event: Optional[str] = None
    quantum_probability: Optional[float] = None
    superposition_created: bool = False
    measurement_triggered: bool = False
    message: str = ""


class LegalMovesResponse(BaseModel):
    """Response containing legal moves for a position."""
    square: str
    legal_moves: list[str]
    quantum_moves: list[str] = []

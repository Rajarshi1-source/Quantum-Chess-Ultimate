"""
Quantum Chess Ultimate - Move Validator

Provides move validation utilities used by the game state manager.
Separates validation logic from the engine for cleaner architecture.
"""

import logging

logger = logging.getLogger(__name__)


class MoveValidator:
    """
    Validates chess moves considering both classical rules
    and quantum state constraints.
    """

    VALID_FILES = set("abcdefgh")
    VALID_RANKS = set("12345678")

    @staticmethod
    def is_valid_square(square: str) -> bool:
        """Check if a square string is valid algebraic notation."""
        return (
            len(square) == 2
            and square[0] in MoveValidator.VALID_FILES
            and square[1] in MoveValidator.VALID_RANKS
        )

    @staticmethod
    def validate_move_format(from_square: str, to_square: str) -> tuple[bool, str]:
        """
        Validate basic move format.
        Returns (is_valid, error_message).
        """
        if not MoveValidator.is_valid_square(from_square):
            return False, f"Invalid source square: {from_square}"
        if not MoveValidator.is_valid_square(to_square):
            return False, f"Invalid target square: {to_square}"
        if from_square == to_square:
            return False, "Source and target squares are the same"
        return True, ""

    @staticmethod
    def is_valid_promotion(piece_type: str) -> bool:
        """Check if a promotion piece type is valid."""
        return piece_type in ("queen", "rook", "bishop", "knight")

    @staticmethod
    def square_to_coords(square: str) -> tuple[int, int]:
        """Convert algebraic notation to (row, col) coordinates."""
        col = ord(square[0]) - ord("a")
        row = int(square[1]) - 1
        return row, col

    @staticmethod
    def coords_to_square(row: int, col: int) -> str:
        """Convert (row, col) coordinates to algebraic notation."""
        return f"{chr(col + ord('a'))}{row + 1}"

    @staticmethod
    def is_same_color_square(sq1: str, sq2: str) -> bool:
        """Check if two squares are the same color on the board."""
        r1, c1 = MoveValidator.square_to_coords(sq1)
        r2, c2 = MoveValidator.square_to_coords(sq2)
        return (r1 + c1) % 2 == (r2 + c2) % 2

    @staticmethod
    def manhattan_distance(sq1: str, sq2: str) -> int:
        """Calculate Manhattan distance between two squares."""
        r1, c1 = MoveValidator.square_to_coords(sq1)
        r2, c2 = MoveValidator.square_to_coords(sq2)
        return abs(r1 - r2) + abs(c1 - c2)

    @staticmethod
    def chebyshev_distance(sq1: str, sq2: str) -> int:
        """Calculate Chebyshev distance (king distance) between squares."""
        r1, c1 = MoveValidator.square_to_coords(sq1)
        r2, c2 = MoveValidator.square_to_coords(sq2)
        return max(abs(r1 - r2), abs(c1 - c2))

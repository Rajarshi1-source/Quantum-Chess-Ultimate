"""
Quantum Chess Ultimate - Position Evaluator

Position evaluation heuristics combining classical chess knowledge
with quantum state analysis.
"""

import logging

logger = logging.getLogger(__name__)

# Piece-square tables for positional evaluation
# Values are from white's perspective; flip for black.

PAWN_TABLE = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

KNIGHT_TABLE = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
]

BISHOP_TABLE = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
]

KING_TABLE_MIDDLEGAME = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
]

PIECE_TABLES = {
    "pawn": PAWN_TABLE,
    "knight": KNIGHT_TABLE,
    "bishop": BISHOP_TABLE,
    "king": KING_TABLE_MIDDLEGAME,
}

PIECE_BASE_VALUES = {
    "empty": 0,
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 500,
    "queen": 900,
    "king": 20000,
}


class PositionEvaluator:
    """
    Evaluates chess positions using classical heuristics
    enhanced with quantum state analysis.
    """

    @staticmethod
    def evaluate(board: dict, superposition_squares: set,
                 entanglement_pairs: list, color: str = "white") -> dict:
        """
        Full position evaluation.

        Returns a dict with classical_score, quantum_score,
        combined_score, and component breakdown.
        """
        material = PositionEvaluator._material_score(board)
        positional = PositionEvaluator._positional_score(board)
        mobility = PositionEvaluator._mobility_score(board)
        quantum = PositionEvaluator._quantum_score(
            board, superposition_squares, entanglement_pairs
        )

        classical_score = material + positional + mobility
        quantum_score = quantum
        combined = classical_score + quantum_score

        # Flip if evaluating for black
        if color == "black":
            classical_score = -classical_score
            quantum_score = -quantum_score
            combined = -combined

        return {
            "classical_score": round(classical_score / 100, 2),
            "quantum_score": round(quantum_score / 100, 2),
            "combined_score": round(combined / 100, 2),
            "components": {
                "material": round(material / 100, 2),
                "positional": round(positional / 100, 2),
                "mobility": round(mobility / 100, 2),
                "quantum": round(quantum / 100, 2),
            },
        }

    @staticmethod
    def _material_score(board: dict) -> float:
        """Calculate material balance."""
        score = 0.0
        for _, piece in board.items():
            value = PIECE_BASE_VALUES.get(piece["type"], 0)
            probability = piece.get("probability", 1.0)
            adjusted = value * probability

            if piece["color"] == "white":
                score += adjusted
            else:
                score -= adjusted
        return score

    @staticmethod
    def _positional_score(board: dict) -> float:
        """Calculate positional score using piece-square tables."""
        score = 0.0
        for square, piece in board.items():
            table = PIECE_TABLES.get(piece["type"])
            if table is None:
                continue

            col = ord(square[0]) - ord("a")
            row = int(square[1]) - 1

            if piece["color"] == "white":
                value = table[7 - row][col]
                score += value
            else:
                value = table[row][col]
                score -= value

        return score * 10  # Scale factor

    @staticmethod
    def _mobility_score(board: dict) -> float:
        """
        Simplified mobility estimate.
        Full mobility requires engine's move generation.
        """
        white_pieces = sum(1 for p in board.values() if p["color"] == "white")
        black_pieces = sum(1 for p in board.values() if p["color"] == "black")
        return (white_pieces - black_pieces) * 10

    @staticmethod
    def _quantum_score(board: dict, superposition_squares: set,
                       entanglement_pairs: list) -> float:
        """
        Evaluate quantum state advantages.

        Superposition pieces provide tactical flexibility.
        Entanglement pairs provide coordination bonuses.
        """
        score = 0.0

        for square in superposition_squares:
            piece = board.get(square, {})
            if not piece:
                continue
            prob = piece.get("probability", 0.5)
            # Uncertainty bonus — superposition provides optionality
            uncertainty_bonus = 50 * (1 - abs(2 * prob - 1))

            if piece.get("color") == "white":
                score += uncertainty_bonus
            else:
                score -= uncertainty_bonus

        # Entanglement coordination bonus
        for sq1, sq2 in entanglement_pairs:
            p1 = board.get(sq1, {})
            p2 = board.get(sq2, {})
            if p1.get("color") == p2.get("color"):
                # Same-color entanglement is advantageous
                bonus = 30
                if p1.get("color") == "white":
                    score += bonus
                else:
                    score -= bonus

        return score

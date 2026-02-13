"""
Quantum Chess Ultimate - Game State Manager

Manages the high-level game state: turn tracking, move history,
captured pieces, and coordinates between the quantum engine and
the move validator.
"""

from typing import Optional
from datetime import datetime
import logging

from app.core.quantum_engine import EnhancedQuantumChessEngine
from app.models.game import (
    GameConfig, GameState, GameStatus, GameMode,
    PieceColor, PieceInfo, PieceType,
)
from app.models.move import Move, MoveResult

logger = logging.getLogger(__name__)


class GameStateManager:
    """
    Manages a single game's lifecycle: initialization, moves,
    quantum operations, and state serialization.
    """

    def __init__(self, game_id: str, config: GameConfig):
        self.game_id = game_id
        self.config = config
        self.engine = EnhancedQuantumChessEngine(
            depth=config.search_depth,
            shots=100,
            superposition_prob=config.quantum_probability,
        )
        self.status: GameStatus = GameStatus.ACTIVE
        self.turn: PieceColor = PieceColor.WHITE
        self.move_count: int = 0
        self.measurement_count: int = 0
        self.move_history: list[dict] = []
        self.captured_pieces: dict[str, list[str]] = {"white": [], "black": []}
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

        # Initialize board
        self.engine.initialize_board()
        logger.info(f"Game {game_id} created with mode={config.mode}")

    def make_move(self, move: Move) -> MoveResult:
        """
        Execute a move on the board.

        In quantum mode, moves may create superpositions or trigger
        measurements depending on the game state.
        """
        from_sq = move.from_square
        to_sq = move.to_square

        # Validate the piece exists and belongs to current player
        piece_data = self.engine.board.get(from_sq)
        if piece_data is None:
            return MoveResult(
                success=False, from_square=from_sq, to_square=to_sq,
                piece_moved="", message="No piece at source square",
            )

        if piece_data["color"] != self.turn.value:
            return MoveResult(
                success=False, from_square=from_sq, to_square=to_sq,
                piece_moved=piece_data["type"],
                message=f"It's {self.turn.value}'s turn",
            )

        # Check if the move is legal
        legal_targets = self.engine.get_legal_moves_for_square(from_sq)
        if to_sq not in legal_targets:
            return MoveResult(
                success=False, from_square=from_sq, to_square=to_sq,
                piece_moved=piece_data["type"],
                message="Illegal move",
            )

        # Check for capture
        captured = self.engine.board.get(to_sq)
        captured_type = captured["type"] if captured else None

        # Quantum events
        quantum_event = None
        superposition_created = False
        measurement_triggered = False

        if self.config.mode in (GameMode.QUANTUM, GameMode.HYBRID):
            # If moving to a superposition square, trigger measurement
            if to_sq in self.engine.superposition_squares:
                self.engine.measure_square(to_sq)
                measurement_triggered = True
                quantum_event = f"Measurement triggered at {to_sq}"
                self.measurement_count += 1

            # If from a superposition square, collapse it first
            if from_sq in self.engine.superposition_squares:
                result = self.engine.measure_square(from_sq)
                measurement_triggered = True
                self.measurement_count += 1
                # Check if the piece survived measurement
                if from_sq not in self.engine.board:
                    return MoveResult(
                        success=True, from_square=from_sq, to_square=to_sq,
                        piece_moved=piece_data["type"],
                        quantum_event="Piece collapsed away during measurement!",
                        measurement_triggered=True,
                        message="Piece dissolved during quantum measurement",
                    )

            # Random quantum superposition events
            import random
            if (self.config.mode == GameMode.QUANTUM and
                    random.random() < self.config.quantum_probability * 0.3):
                superposition_created = True
                quantum_event = f"Quantum superposition created at {to_sq}"

        # Execute the move
        if captured_type:
            self.captured_pieces[piece_data["color"]].append(captured_type)

        self.engine._apply_move(from_sq, to_sq)

        # Handle pawn promotion
        if piece_data["type"] == "pawn":
            row = int(to_sq[1])
            if (piece_data["color"] == "white" and row == 8) or \
               (piece_data["color"] == "black" and row == 1):
                promo = move.promotion or "queen"
                self.engine.board[to_sq]["type"] = promo

        # Apply superposition if triggered
        if superposition_created:
            self.engine.create_superposition(to_sq)

        # Record move
        self.move_history.append({
            "move_number": self.move_count + 1,
            "from": from_sq,
            "to": to_sq,
            "piece": piece_data["type"],
            "color": piece_data["color"],
            "captured": captured_type,
            "quantum_event": quantum_event,
        })

        self.move_count += 1
        self.updated_at = datetime.now()

        # Switch turns
        self.turn = PieceColor.BLACK if self.turn == PieceColor.WHITE else PieceColor.WHITE

        # Check game-ending conditions
        is_check = self.engine._is_in_check(self.turn.value)
        opponent_moves = self.engine.get_all_legal_moves(self.turn.value)

        is_checkmate = False
        is_stalemate = False

        if not opponent_moves:
            if is_check:
                is_checkmate = True
                self.status = GameStatus.CHECKMATE
            else:
                is_stalemate = True
                self.status = GameStatus.STALEMATE
        elif is_check:
            self.status = GameStatus.CHECK

        return MoveResult(
            success=True,
            from_square=from_sq,
            to_square=to_sq,
            piece_moved=piece_data["type"],
            piece_captured=captured_type,
            is_check=is_check,
            is_checkmate=is_checkmate,
            is_stalemate=is_stalemate,
            quantum_event=quantum_event,
            superposition_created=superposition_created,
            measurement_triggered=measurement_triggered,
            message="Move executed successfully",
        )

    def get_state(self) -> GameState:
        """Serialize current game state into a GameState model."""
        position = {}
        for square, piece in self.engine.board.items():
            position[square] = PieceInfo(
                type=PieceType(piece["type"]),
                color=PieceColor(piece["color"]),
                in_superposition=piece.get("in_superposition", False),
                superposition_probability=piece.get("probability", 1.0),
            )

        return GameState(
            game_id=self.game_id,
            mode=self.config.mode,
            status=self.status,
            turn=self.turn,
            position=position,
            move_count=self.move_count,
            measurement_count=self.measurement_count,
            quantum_probability=self.config.quantum_probability,
            superposition_squares=list(self.engine.superposition_squares),
            entanglement_pairs=[
                (a, b) for a, b in self.engine.entanglement_pairs
            ],
            move_history=self.move_history,
            captured_pieces=self.captured_pieces,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def get_legal_moves(self, square: str) -> list[str]:
        """Get legal moves for a piece at the given square."""
        return self.engine.get_legal_moves_for_square(square)

    def get_all_legal_moves_for_current_player(self) -> dict[str, list[str]]:
        """Get all legal moves for the current player."""
        moves = {}
        for square, piece in self.engine.board.items():
            if piece["color"] == self.turn.value:
                targets = self.engine.get_legal_moves_for_square(square)
                if targets:
                    moves[square] = targets
        return moves

    def measure_square(self, square: str) -> dict:
        """Measure a specific square."""
        result = self.engine.measure_square(square)
        self.measurement_count += 1
        self.updated_at = datetime.now()
        return result

    def measure_all(self) -> dict[str, dict]:
        """Measure all superposition squares."""
        results = self.engine.measure_all()
        self.measurement_count += len(results)
        self.updated_at = datetime.now()
        return results

    def find_best_move(self) -> dict:
        """Find best move using AI."""
        return self.engine.find_best_move(self.turn.value)

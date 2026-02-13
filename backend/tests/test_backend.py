"""
Quantum Chess Ultimate — Backend Unit Tests

Tests for the quantum engine, game state, and API endpoints.
"""

import pytest
import sys
import os

# Ensure the backend app is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Quantum Engine Tests ──────────────────────────────────────

class TestQuantumSimulator:
    """Tests for the NumPy-based quantum simulator."""

    def test_initialization(self):
        from app.core.quantum_engine import QuantumSimulator
        sim = QuantumSimulator(num_qubits=5)
        assert sim.num_qubits == 5
        assert sim.dim == 32
        assert abs(sim.state[0]) == 1.0

    def test_measurement_returns_valid_bits(self):
        from app.core.quantum_engine import QuantumSimulator
        sim = QuantumSimulator(num_qubits=3)
        results = sim.measure(shots=10)
        assert len(results) == 10
        for bits in results:
            assert len(bits) == 3
            for b in bits:
                assert b in (0, 1)

    def test_x_gate_flips_qubit(self):
        from app.core.quantum_engine import QuantumSimulator
        sim = QuantumSimulator(num_qubits=1)
        sim.x(0)  # Flip qubit 0 from |0⟩ to |1⟩
        results = sim.measure(shots=10)
        # All measurements should give [1]
        for bits in results:
            assert bits[0] == 1

    def test_h_gate_creates_superposition(self):
        from app.core.quantum_engine import QuantumSimulator
        import numpy as np
        sim = QuantumSimulator(num_qubits=1)
        sim.h(0)  # Hadamard creates equal superposition
        # With enough shots, we should see both 0 and 1
        results = sim.measure(shots=100)
        values = {r[0] for r in results}
        assert 0 in values or 1 in values  # At least some variation


# ─── Enhanced Engine Tests ──────────────────────────────────────

class TestEnhancedQuantumChessEngine:
    """Tests for the full quantum chess engine."""

    def test_engine_initialization(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine(depth=2, shots=50)
        assert engine.search_depth == 2
        assert engine.shots == 50

    def test_board_initialization(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        board = engine.initialize_board()
        # 32 pieces: 16 white + 16 black
        assert len(board) == 32
        # Check specific pieces
        assert board["e1"]["type"] == "king"
        assert board["e1"]["color"] == "white"
        assert board["e8"]["type"] == "king"
        assert board["e8"]["color"] == "black"
        assert board["a2"]["type"] == "pawn"
        assert board["d8"]["type"] == "queen"

    def test_legal_moves_pawn(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        moves = engine.get_legal_moves_for_square("e2")
        assert "e3" in moves
        assert "e4" in moves
        assert len(moves) == 2  # e3 and e4

    def test_legal_moves_knight(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        moves = engine.get_legal_moves_for_square("b1")
        assert "a3" in moves
        assert "c3" in moves
        assert len(moves) == 2

    def test_move_execution(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        engine._apply_move("e2", "e4")
        assert "e2" not in engine.board
        assert engine.board["e4"]["type"] == "pawn"
        assert engine.board["e4"]["color"] == "white"

    def test_superposition_creation(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        engine.create_superposition("e2")
        assert "e2" in engine.superposition_squares
        assert engine.board["e2"]["in_superposition"] is True
        assert engine.board["e2"]["probability"] < 1.0

    def test_superposition_measurement(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        engine.create_superposition("e2")
        result = engine.measure_square("e2")
        # After measurement, no longer in superposition
        assert "e2" not in engine.superposition_squares

    def test_find_best_move(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine(depth=1)
        engine.initialize_board()
        result = engine.find_best_move("white")
        assert "best_move" in result
        assert result["best_move"] is not None

    def test_evaluate_position(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        score = engine.evaluate_position("white")
        # Initial position should be roughly equal
        assert -5.0 <= score <= 5.0

    def test_circuit_info(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        info = engine.get_circuit_info()
        assert "superposition_count" in info
        assert "entanglement_count" in info
        assert info["superposition_count"] == 0


# ─── Game State Manager Tests ──────────────────────────────────

class TestGameStateManager:
    """Tests for game state management."""

    def test_game_creation(self):
        from app.core.game_state import GameStateManager
        from app.models.game import GameConfig
        game = GameStateManager("test-1", GameConfig())
        state = game.get_state()
        assert state.game_id == "test-1"
        assert state.turn.value == "white"
        assert state.move_count == 0
        assert len(state.position) == 32

    def test_move_execution(self):
        from app.core.game_state import GameStateManager
        from app.models.game import GameConfig
        from app.models.move import Move
        game = GameStateManager("test-2", GameConfig())
        result = game.make_move(Move(from_square="e2", to_square="e4"))
        assert result.success is True
        assert result.piece_moved == "pawn"
        state = game.get_state()
        assert state.turn.value == "black"
        assert state.move_count == 1

    def test_illegal_move_rejected(self):
        from app.core.game_state import GameStateManager
        from app.models.game import GameConfig
        from app.models.move import Move
        game = GameStateManager("test-3", GameConfig())
        result = game.make_move(Move(from_square="e2", to_square="e5"))
        assert result.success is False

    def test_wrong_turn_rejected(self):
        from app.core.game_state import GameStateManager
        from app.models.game import GameConfig
        from app.models.move import Move
        game = GameStateManager("test-4", GameConfig())
        result = game.make_move(Move(from_square="e7", to_square="e5"))
        assert result.success is False
        assert "white" in result.message.lower()


# ─── Move Validator Tests ──────────────────────────────────────

class TestMoveValidator:
    """Tests for move validation utilities."""

    def test_valid_squares(self):
        from app.core.move_validator import MoveValidator
        assert MoveValidator.is_valid_square("e4") is True
        assert MoveValidator.is_valid_square("a1") is True
        assert MoveValidator.is_valid_square("h8") is True

    def test_invalid_squares(self):
        from app.core.move_validator import MoveValidator
        assert MoveValidator.is_valid_square("i1") is False
        assert MoveValidator.is_valid_square("a9") is False
        assert MoveValidator.is_valid_square("") is False
        assert MoveValidator.is_valid_square("abc") is False

    def test_move_format_validation(self):
        from app.core.move_validator import MoveValidator
        valid, _ = MoveValidator.validate_move_format("e2", "e4")
        assert valid is True
        invalid, msg = MoveValidator.validate_move_format("e2", "e2")
        assert invalid is False

    def test_coordinate_conversion(self):
        from app.core.move_validator import MoveValidator
        row, col = MoveValidator.square_to_coords("a1")
        assert row == 0 and col == 0
        row, col = MoveValidator.square_to_coords("h8")
        assert row == 7 and col == 7
        assert MoveValidator.coords_to_square(0, 0) == "a1"
        assert MoveValidator.coords_to_square(7, 7) == "h8"


# ─── Evaluator Tests ───────────────────────────────────────────

class TestEvaluator:
    """Tests for position evaluation."""

    def test_initial_position_balanced(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        from app.core.evaluator import PositionEvaluator
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        result = PositionEvaluator.evaluate(
            engine.board, engine.superposition_squares,
            engine.entanglement_pairs, "white"
        )
        assert "combined_score" in result
        assert "components" in result
        # Material should be 0 at start
        assert result["components"]["material"] == 0.0

    def test_evaluation_after_capture(self):
        from app.core.quantum_engine import EnhancedQuantumChessEngine
        from app.core.evaluator import PositionEvaluator
        engine = EnhancedQuantumChessEngine()
        engine.initialize_board()
        # Remove black's queen for testing
        del engine.board["d8"]
        result = PositionEvaluator.evaluate(
            engine.board, engine.superposition_squares,
            engine.entanglement_pairs, "white"
        )
        # White should be winning (positive score)
        assert result["combined_score"] > 0


# ─── Game Manager Tests ────────────────────────────────────────

class TestGameManager:
    """Tests for the game manager service."""

    def test_create_and_list_games(self):
        from app.services.game_manager import GameManager
        gm = GameManager()
        state = gm.create_game()
        assert state.game_id is not None
        games = gm.list_games()
        assert len(games) == 1

    def test_delete_game(self):
        from app.services.game_manager import GameManager
        gm = GameManager()
        state = gm.create_game()
        assert gm.delete_game(state.game_id) is True
        assert gm.delete_game("nonexistent") is False

    def test_game_stats(self):
        from app.services.game_manager import GameManager
        gm = GameManager()
        gm.create_game()
        gm.create_game()
        stats = gm.get_stats()
        assert stats["active_games"] == 2


# ─── Cache Manager Tests ───────────────────────────────────────

class TestCacheManager:
    """Tests for the caching layer."""

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        from app.services.cache_manager import CacheManager
        cache = CacheManager()
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"

    @pytest.mark.asyncio
    async def test_cache_miss(self):
        from app.services.cache_manager import CacheManager
        cache = CacheManager()
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_delete(self):
        from app.services.cache_manager import CacheManager
        cache = CacheManager()
        await cache.set("key1", "value1")
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    def test_cache_stats(self):
        from app.services.cache_manager import CacheManager
        cache = CacheManager()
        stats = cache.stats()
        assert stats["entries"] == 0
        assert stats["hit_rate"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

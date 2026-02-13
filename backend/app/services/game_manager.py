"""
Quantum Chess Ultimate - Game Manager Service

High-level service coordinating game lifecycle.
Manages multiple concurrent games with unique IDs.
"""

import uuid
import logging
from typing import Optional

from app.core.game_state import GameStateManager
from app.models.game import GameConfig, GameState, GameSummary, GameStatus
from app.models.move import Move, MoveResult
from app.services.cache_manager import CacheManager

logger = logging.getLogger(__name__)


class GameManager:
    """
    Manages all active game instances.
    Thread-safe game storage with cache integration.
    """

    def __init__(self, cache: Optional[CacheManager] = None):
        self.games: dict[str, GameStateManager] = {}
        self.cache = cache or CacheManager()
        logger.info("GameManager initialized")

    def create_game(self, config: Optional[GameConfig] = None) -> GameState:
        """Create a new game and return its initial state."""
        game_id = str(uuid.uuid4())[:8]
        cfg = config or GameConfig()
        game = GameStateManager(game_id, cfg)
        self.games[game_id] = game
        logger.info(f"Game created: {game_id}")
        return game.get_state()

    def get_game(self, game_id: str) -> Optional[GameStateManager]:
        """Get a game instance by ID."""
        return self.games.get(game_id)

    def get_state(self, game_id: str) -> Optional[GameState]:
        """Get game state by ID."""
        game = self.games.get(game_id)
        return game.get_state() if game else None

    def make_move(self, game_id: str, move: Move) -> Optional[MoveResult]:
        """Execute a move in a game."""
        game = self.games.get(game_id)
        if not game:
            return None
        return game.make_move(move)

    def get_legal_moves(self, game_id: str, square: str) -> Optional[list[str]]:
        """Get legal moves for a square in a game."""
        game = self.games.get(game_id)
        if not game:
            return None
        return game.get_legal_moves(square)

    def get_all_legal_moves(self, game_id: str) -> Optional[dict]:
        """Get all legal moves for the current player."""
        game = self.games.get(game_id)
        if not game:
            return None
        return game.get_all_legal_moves_for_current_player()

    def delete_game(self, game_id: str) -> bool:
        """Delete a game."""
        if game_id in self.games:
            del self.games[game_id]
            logger.info(f"Game deleted: {game_id}")
            return True
        return False

    def list_games(self) -> list[GameSummary]:
        """List all active games."""
        summaries = []
        for game_id, game in self.games.items():
            state = game.get_state()
            summaries.append(GameSummary(
                game_id=state.game_id,
                mode=state.mode,
                status=state.status,
                turn=state.turn,
                move_count=state.move_count,
                player_white=game.config.player_white,
                player_black=game.config.player_black,
                created_at=state.created_at,
            ))
        return summaries

    def measure_square(self, game_id: str, square: str) -> Optional[dict]:
        """Measure a quantum square."""
        game = self.games.get(game_id)
        if not game:
            return None
        return game.measure_square(square)

    def measure_all(self, game_id: str) -> Optional[dict]:
        """Measure all quantum squares."""
        game = self.games.get(game_id)
        if not game:
            return None
        return game.measure_all()

    def find_best_move(self, game_id: str) -> Optional[dict]:
        """Find best move using AI."""
        game = self.games.get(game_id)
        if not game:
            return None
        return game.find_best_move()

    def get_stats(self) -> dict:
        """Get manager statistics."""
        return {
            "active_games": len(self.games),
            "cache_stats": self.cache.stats(),
        }

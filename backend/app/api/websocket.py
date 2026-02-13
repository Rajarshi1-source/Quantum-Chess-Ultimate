"""
Quantum Chess Ultimate - WebSocket Handler

Manages real-time WebSocket connections for live game updates.
"""

import json
import logging
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections per game."""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, game_id: str, websocket: WebSocket):
        """Accept and register a WebSocket connection for a game."""
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
        self.active_connections[game_id].append(websocket)
        logger.info(f"WebSocket connected for game {game_id}")

    def disconnect(self, game_id: str, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                del self.active_connections[game_id]
        logger.info(f"WebSocket disconnected for game {game_id}")

    async def broadcast(self, game_id: str, message: dict):
        """Broadcast a message to all connections for a game."""
        if game_id not in self.active_connections:
            return

        dead_connections = []
        for connection in self.active_connections[game_id]:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        for conn in dead_connections:
            self.active_connections[game_id].remove(conn)

    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send a message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send personal message: {e}")

    def get_connection_count(self, game_id: str) -> int:
        """Get number of active connections for a game."""
        return len(self.active_connections.get(game_id, []))

    def get_total_connections(self) -> int:
        """Get total active connections across all games."""
        return sum(len(conns) for conns in self.active_connections.values())


async def handle_websocket_message(
    game_id: str, data: dict, game_manager, ws_manager: ConnectionManager
):
    """
    Process incoming WebSocket messages.

    Supported message types:
    - move: Execute a move
    - measure: Trigger quantum measurement
    - evaluate: Request position evaluation
    - legal_moves: Request legal moves for a square
    - state: Request current game state
    """
    msg_type = data.get("type", "")

    if msg_type == "move":
        from app.models.move import Move
        move = Move(
            from_square=data.get("from", ""),
            to_square=data.get("to", ""),
            promotion=data.get("promotion"),
        )
        result = game_manager.make_move(game_id, move)
        if result:
            response = {
                "type": "move_result",
                "data": result.model_dump(),
            }
            await ws_manager.broadcast(game_id, response)

            # Also send updated state
            state = game_manager.get_state(game_id)
            if state:
                await ws_manager.broadcast(game_id, {
                    "type": "state_update",
                    "data": state.model_dump(mode="json"),
                })

    elif msg_type == "measure":
        square = data.get("square")
        if square:
            result = game_manager.measure_square(game_id, square)
        else:
            result = game_manager.measure_all(game_id)
        await ws_manager.broadcast(game_id, {
            "type": "measurement_result",
            "data": result,
        })

    elif msg_type == "evaluate":
        game = game_manager.get_game(game_id)
        if game:
            from app.core.evaluator import PositionEvaluator
            eval_result = PositionEvaluator.evaluate(
                board=game.engine.board,
                superposition_squares=game.engine.superposition_squares,
                entanglement_pairs=game.engine.entanglement_pairs,
                color=game.turn.value,
            )
            await ws_manager.broadcast(game_id, {
                "type": "evaluation",
                "data": eval_result,
            })

    elif msg_type == "legal_moves":
        square = data.get("square", "")
        moves = game_manager.get_legal_moves(game_id, square)
        await ws_manager.broadcast(game_id, {
            "type": "legal_moves",
            "data": {"square": square, "moves": moves or []},
        })

    elif msg_type == "state":
        state = game_manager.get_state(game_id)
        if state:
            await ws_manager.broadcast(game_id, {
                "type": "state_update",
                "data": state.model_dump(mode="json"),
            })

    else:
        logger.warning(f"Unknown WebSocket message type: {msg_type}")

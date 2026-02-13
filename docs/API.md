# Quantum Chess Ultimate — API Reference

## Base URL

| Environment | URL |
|---|---|
| Development | `http://localhost:8000` |
| Docker Compose | `http://localhost:8000` |

---

## Authentication

No authentication required for v1.0. All endpoints are public.

---

## Game Endpoints

### `POST /api/game/new`

Create a new game.

**Request Body:**
```json
{
  "mode": "quantum",          // "classical" | "quantum" | "hybrid" | "tutorial"
  "quantum_probability": 0.5, // 0.0–1.0, chance of quantum effects
  "search_depth": 3,          // AI search depth (1–6)
  "player_white": "Player 1",
  "player_black": "Player 2"
}
```

**Response:** `GameCreateResponse`
```json
{
  "game_id": "abc123",
  "state": { /* GameState */ },
  "message": "Game created successfully"
}
```

---

### `GET /api/game/{game_id}`

Get current game state.

**Response:** `GameState`
```json
{
  "game_id": "abc123",
  "mode": "quantum",
  "status": "active",
  "turn": "white",
  "position": {
    "e2": { "type": "pawn", "color": "white", "in_superposition": false, "superposition_probability": 1.0 }
  },
  "move_count": 0,
  "superposition_squares": [],
  "entanglement_pairs": [],
  "move_history": [],
  "captured_pieces": { "white": [], "black": [] }
}
```

---

### `POST /api/game/{game_id}/move`

Execute a move.

**Request Body:**
```json
{
  "from_square": "e2",
  "to_square": "e4",
  "promotion": null    // "queen" | "rook" | "bishop" | "knight" when promoting
}
```

**Response:** `MoveResult`
```json
{
  "success": true,
  "message": "Move executed",
  "move": "e2e4",
  "captured_piece": null,
  "quantum_event": null,    // "superposition_created" | "measurement_triggered" | null
  "new_state": { /* GameState */ }
}
```

---

### `GET /api/game/{game_id}/legal-moves/{square}`

Get legal moves for a piece on the given square.

**Response:**
```json
{
  "square": "e2",
  "legal_moves": ["e3", "e4"]
}
```

---

### `DELETE /api/game/{game_id}`

Delete a game.

**Response:**
```json
{
  "message": "Game abc123 deleted"
}
```

---

## Quantum Endpoints

### `POST /api/quantum/{game_id}/evaluate`

Evaluate the current position using quantum-enhanced analysis.

**Response:** `QuantumEvaluation`
```json
{
  "classical_score": 0.25,
  "quantum_score": 0.15,
  "combined_score": 0.40,
  "best_move": "e2e4",
  "superpositions": 2,
  "entanglements": 1,
  "measurement_probability": 0.85
}
```

---

### `GET /api/quantum/{game_id}/best-move`

Get the best move from the quantum-enhanced AI.

**Response:**
```json
{
  "best_move": "e2e4",
  "evaluation": 0.40,
  "depth": 3
}
```

---

### `POST /api/quantum/{game_id}/measure`

Measure (collapse) all superpositions on the board.

**Response:**
```json
{
  "measured_squares": ["d4", "f5"],
  "results": {
    "d4": { "type": "pawn", "color": "white" },
    "f5": null
  },
  "new_state": { /* GameState */ }
}
```

---

### `GET /api/quantum/{game_id}/circuit`

Get quantum circuit information for the current state.

**Response:** `CircuitInfo`
```json
{
  "total_qubits": 10,
  "circuit_depth": 5,
  "gate_count": 12,
  "gates_used": ["H", "X", "CNOT"],
  "optimization_suggestions": []
}
```

---

## Analysis Endpoints

### `POST /api/analysis/{game_id}/position`

Get detailed position analysis breakdown.

**Response:**
```json
{
  "white": { "material": 39, "positional": 0.15, "total": 39.15 },
  "black": { "material": 39, "positional": -0.10, "total": 38.90 },
  "advantage": 0.25,
  "phase": "opening"
}
```

---

### `GET /api/analysis/{game_id}/history`

Get move history.

**Response:**
```json
{
  "move_count": 5,
  "moves": [
    { "move": "e2e4", "turn": "white", "quantum_event": null },
    { "move": "e7e5", "turn": "black", "quantum_event": "superposition_created" }
  ]
}
```

---

## Utility Endpoints

### `GET /health`

Health check.

```json
{ "status": "healthy", "environment": "development" }
```

### `GET /`

Root endpoint with API information.

### `GET /stats`

Active games and cache statistics.

---

## WebSocket

### `WS /ws/{game_id}`

Real-time game updates.

**Client → Server messages:**
```json
{ "type": "move", "data": { "from_square": "e2", "to_square": "e4" } }
{ "type": "measure", "data": {} }
{ "type": "evaluate", "data": {} }
{ "type": "get_state", "data": {} }
```

**Server → Client messages:**
```json
{ "type": "state_update", "data": { /* GameState */ } }
{ "type": "move_result", "data": { /* MoveResult */ } }
{ "type": "evaluation", "data": { /* QuantumEvaluation */ } }
{ "type": "error", "data": { "message": "..." } }
```

---

## Error Responses

All errors follow:
```json
{
  "detail": "Error description"
}
```

| Status Code | Meaning |
|---|---|
| 400 | Invalid request (bad move, invalid square) |
| 404 | Game not found |
| 422 | Validation error (invalid body) |
| 500 | Internal server error |

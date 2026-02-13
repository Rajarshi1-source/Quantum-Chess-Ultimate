# Quantum Chess Ultimate — User Guide

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 22+
- npm 10+

### 1. Start the Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

Verify: open `http://localhost:8000/health` — should show `{"status":"healthy"}`.

### 2. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### 3. Using Docker (Alternative)

```bash
docker compose up -d
```

Open `http://localhost:3000`.

---

## Playing the Game

### Creating a New Game

1. Select a **game mode** from the dropdown:
   - **Quantum** — Full quantum mechanics
   - **Classical** — Standard chess
   - **Hybrid** — Occasional quantum events
2. Click **⚛ Start**
3. The board will appear with all 32 pieces in starting position

### Making Moves

1. **Click a piece** — the square highlights cyan, and legal move targets appear as dots
2. **Click a target square** — the move is executed
3. If a quantum event triggers, a toast notification appears at the bottom

### Quantum Controls (Left Sidebar)

- **Quantum Metrics** — Live count of superpositions, entanglements, and measurements
- **Circuit Info** — Quantum circuit details (qubits, depth, gates)
- **Measure All** — Collapses all superpositions to definite states

### Analysis Panel (Right Sidebar)

- **Status** — Current game status (active, check, checkmate, etc.)
- **Evaluation** — Classical, quantum, and combined position scores
- **Best Move** — AI-suggested optimal move (click "Find Best" to compute)
- **Captured Pieces** — Pieces taken by each side
- **Move History** — Scrollable list with quantum event markers

---

## Keyboard Shortcuts (Desktop App)

| Shortcut | Action |
|---|---|
| `Ctrl+N` | New Game |
| `Ctrl+S` | Save Game |
| `Ctrl+O` | Load Game |
| `Ctrl+Shift+E` | Export PGN |
| `Ctrl+Z` | Undo Move |
| `Ctrl+Shift+Z` | Redo Move |
| `F` | Flip Board |
| `Q` | Toggle Quantum Overlay |
| `M` | Measure All |
| `Ctrl+Shift+A` | Request AI Move |
| `Ctrl+Q` | Quit |

---

## Game Modes Explained

| Mode | Quantum Chance | Best For |
|---|---|---|
| **Classical** | 0% | Learning standard chess |
| **Hybrid** | ~50% | Balanced experience |
| **Quantum** | 100% | Full quantum immersion |

---

## Understanding the Board

| Visual Element | Meaning |
|---|---|
| **Cyan border** | Selected square |
| **Green dots** | Legal move targets |
| **Red glow** | King in check |
| **Ghosted piece** | Piece in superposition |
| **Probability badge** | Chance piece is on this square |
| **Purple connecting lines** | Entangled pairs |
| **Last move highlight** | Origin and destination of previous move |

---

## Saving and Loading (Desktop Only)

- **Save**: `Ctrl+S` → Choose file location → Saves as `.json`
- **Load**: `Ctrl+O` → Select a saved `.json` file
- **Export PGN**: `Ctrl+Shift+E` → Export move history as `.pgn`

Save files include the full game state, quantum states, and move history.

---

## API Access

The backend exposes a REST API at `http://localhost:8000`. See [API.md](./API.md) for the full reference.

Swagger UI is available at `http://localhost:8000/docs`.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Backend won't start | Check Python 3.12+ is installed; verify `pip install -r requirements.txt` completed |
| Frontend shows "connection error" | Ensure backend is running on port 8000 |
| Moves don't execute | Check game is active (not checkmate/stalemate) and it's the correct turn |
| Docker build fails | Ensure Docker Desktop is running; try `docker system prune` then rebuild |
| Quantum effects not appearing | Verify game mode is "quantum" or "hybrid", not "classical" |

---

## Project Structure

```
Quantum_Chess_Ultimate/
├── backend/             # FastAPI backend
│   ├── app/
│   │   ├── api/         # REST + WebSocket endpoints
│   │   ├── core/        # Engine, game state, evaluator
│   │   ├── models/      # Pydantic data models
│   │   └── services/    # Game manager, cache, optimizer
│   ├── tests/           # Backend tests (pytest)
│   └── Dockerfile
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── components/  # Board, Controls, Analysis
│   │   ├── store/       # Zustand state stores
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript definitions
│   └── Dockerfile
├── desktop/             # Electron desktop wrapper
│   └── electron/        # Main process, preload, IPC
├── docs/                # Documentation
├── e2e/                 # Playwright E2E tests
└── docker-compose.yml
```

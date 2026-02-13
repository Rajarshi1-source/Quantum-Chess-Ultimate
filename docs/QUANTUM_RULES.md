# Quantum Chess Rules

Quantum Chess extends classical chess with concepts from quantum mechanics. Pieces can exist in **superposition** (multiple states simultaneously), become **entangled** with each other, and require **measurement** to collapse into definite states.

---

## Core Concepts

### 1. Superposition

When a quantum event triggers (based on the game's `quantum_probability` setting), a piece can enter **superposition** — it exists on multiple squares simultaneously with a combined probability of 1.0.

- A piece in superposition appears ghosted/translucent on the board
- Each potential position has an associated probability (e.g., 60% on d4, 40% on f5)
- Superposed pieces can still be captured, but the outcome is probabilistic
- King cannot enter superposition (to maintain check/checkmate integrity)

### 2. Measurement

Measurement **collapses** a superposition into a single definite state:

- **Automatic measurement**: Moving to or from a superposed square triggers measurement
- **Manual measurement**: Players can measure all superpositions using the "Measure All" action
- **Outcome**: The piece collapses to one of its potential positions based on probabilities
- After measurement, the piece behaves classically until it enters superposition again

### 3. Entanglement

When two pieces interact during a quantum event, they can become **entangled**:

- Measuring one entangled piece affects the other's state
- Entangled pairs are tracked and displayed in the quantum controls panel
- Capturing an entangled piece affects its partner

---

## Game Modes

| Mode | Quantum Effects | Description |
|------|:-:|---|
| **Classical** | ✗ | Standard chess, no quantum mechanics |
| **Quantum** | ✓ | Full quantum effects on every move |
| **Hybrid** | ½ | Quantum effects triggered probabilistically |
| **Tutorial** | ✓ | Quantum chess with move explanations |

---

## How Quantum Events Trigger

In **Quantum** and **Hybrid** modes, each move has a chance to create a quantum event:

1. **Move is executed** normally (piece moves from A to B)
2. **Quantum probability check**: A random value is compared to the game's `quantum_probability` setting (default: 50%)
3. If triggered, one of these events occurs:
   - **Superposition created**: The moved piece enters superposition across its current and a related square
   - **Measurement triggered**: An existing superposition on the board collapses
   - **Entanglement formed**: Two nearby pieces become entangled

---

## Impact on Strategy

### Superposition Considerations
- Pieces in superposition control **more squares** (both potential positions)
- But captures are **uncertain** — you might capture empty space
- Creating superpositions near the opponent's king creates strategic uncertainty

### Measurement Timing
- Measure **early** to get certainty before a critical exchange
- Measure **late** to keep your opponent guessing
- Forced measurements (from captures) can be strategically devastating

### Entanglement Tactics
- Entangled pieces create **correlated outcomes** — use this to your advantage
- Sacrificing an entangled piece can affect its partner's position

---

## Evaluation Scoring

The game engine evaluates positions using a combined score:

- **Classical Score**: Standard material + positional evaluation
- **Quantum Score**: Superposition advantage, entanglement value, measurement probability
- **Combined Score**: Weighted combination (higher = better for the side to move)

---

## Differences from Classical Chess

| Feature | Classical | Quantum |
|---|---|---|
| Piece position | Definite | Can be in superposition |
| Captures | Deterministic | Probabilistic when superposed |
| Piece interactions | Independent | Can be entangled |
| Board state | Fully known | Partially observable |
| Strategy depth | Combinatorial | Combinatorial + probabilistic |

---

## Notation

Quantum events are shown in move history with special markers:

| Marker | Meaning |
|---|---|
| `⚛` | Quantum event occurred |
| `Ψ` | Superposition created |
| `📏` | Measurement performed |
| `🔗` | Entanglement formed |

---

## Tips for Beginners

1. **Start with Hybrid mode** — quantum events are less frequent, easier to learn
2. **Watch the probability badges** — they show how likely a superposed piece is on each square
3. **Use Measure All strategically** — don't waste measurements when they benefit you less
4. **The AI considers quantum states** — the evaluation accounts for superposition and entanglement
5. **Experiment!** — The best way to learn quantum chess is to play and observe

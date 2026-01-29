# Quantum Chess Ultimate — Design Document

## 1. Design Goals

The primary objective of Quantum Chess Ultimate is to explore how
**quantum mechanical principles** can be applied to strategic game AI.

Key goals:
- Conceptual correctness over physical accuracy
- Clear abstraction boundaries
- Extensibility for research
- Compatibility with classical AI techniques

---

## 2. Board Representation

Each chess square is modeled as a **5-qubit quantum register**:

| Qubit Index | Meaning |
|-----------|--------|
| 0–2 | Piece type |
| 3 | Piece color |
| 4 | Superposition control |

This allows both classical certainty and quantum uncertainty to coexist.

---

## 3. Move Encoding Strategy

Moves are encoded as **quantum circuits**, not state mutations.

Design principles:
- Moves are reversible (conceptually)
- Probabilistic outcomes are encoded via rotations
- Controlled swaps preserve piece identity

This allows one move to represent multiple possible futures.

---

## 4. Measurement Philosophy

- Measurement collapses quantum states into classical information
- Measurement is deferred until evaluation
- Each evaluation represents one sampled reality

This mirrors real quantum uncertainty while remaining computationally feasible.

---

## 5. Search Strategy

The engine uses a **quantum-aware minimax** algorithm:

- Branches represent probabilistic futures
- Alpha–beta pruning limits combinatorial explosion
- Evaluation occurs post-measurement

This balances exploration depth with quantum simulation cost.

---

## 6. Known Limitations

- No persistent entanglement modeling
- No partial measurement reuse
- Simplified legality checking
- High computational cost

These are deliberate tradeoffs to keep the system explorable.

---

## 7. Future Directions

- Entangled piece representations
- Interference-based capture resolution
- Hybrid classical–quantum evaluation
- Learning-based heuristics

---

## 8. Design Philosophy Summary

Quantum Chess Ultimate is not an attempt to “solve chess with quantum computing.”
It is an exploration of how **uncertainty changes decision-making**.

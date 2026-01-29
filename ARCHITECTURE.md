# Quantum Chess Ultimate — System Architecture

This document describes the **structural and runtime architecture**
of the Quantum Chess Ultimate engine.

---

## 1. High-Level Architecture

The engine follows a **layered, controller-centric design**.

```mermaid
flowchart TD
    A[QuantumChessEngine] --> B[Quantum Board Layer]
    A --> C[Move Generation Layer]
    A --> D[Search Layer]
    D --> E[Evaluation Layer]
    E --> F[Measurement Layer]

    F --> G[QASM Simulator]
    G --> E

2. Component Responsibilities
2.1 QuantumChessEngine (Controller)

Orchestrates all subsystems

Maintains search depth and simulator backend

Entry point for decision-making

2.2 Quantum Board Layer

Represents each board square as a 5-qubit register

Encodes:

Piece identity

Color

Superposition state

Does not enforce rules or legality

2.3 Move Generation Layer

Generates quantum circuits representing moves

Uses:

RY rotations → probabilistic branching

CSWAP gates → information transfer

Produces circuits, not state mutations

2.4 Search Layer

Implements quantum-aware minimax

Handles probabilistic outcomes

Applies alpha–beta pruning to limit branching

2.5 Evaluation Layer

Scores measured board states

Combines:

Material balance

Positional heuristics

Quantum superposition weighting

2.6 Measurement Layer

Collapses quantum states via measurement

Produces classical bitstrings

Represents one sampled reality per evaluation

3. Runtime Flow

sequenceDiagram
    participant Engine
    participant MoveGen
    participant Search
    participant Eval
    participant Simulator

    Engine->>MoveGen: Generate quantum moves
    Engine->>Search: Explore move tree
    Search->>Eval: Request evaluation
    Eval->>Simulator: Measure board
    Simulator-->>Eval: Classical bits
    Eval-->>Search: Score
    Search-->>Engine: Best move

4. Architectural Tradeoffs

| Decision                     | Rationale                    |
| ---------------------------- | ---------------------------- |
| Measurement-based evaluation | Reflects quantum uncertainty |
| Simulator backend            | Hardware-independent         |
| Single-sample evaluation     | Computational feasibility    |
| Layer separation             | Research extensibility       |

5. Future Architectural Extensions

Persistent entanglement layer

Partial measurement caching

Hybrid classical–quantum evaluators

Distributed simulation

Summary:
This architecture prioritizes clarity, extensibility, and research flexibility over raw performance.
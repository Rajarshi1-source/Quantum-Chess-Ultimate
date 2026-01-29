# ♟️ Quantum Chess Ultimate
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-Quantum%20SDK-purple.svg)
![Research](https://img.shields.io/badge/Project-Research%20%26%20Experimental-orange.svg)
![Status](https://img.shields.io/badge/Status-Active%20Development-success.svg)

## 📄 Abstract

Quantum Chess Ultimate presents an experimental framework for integrating
quantum computing concepts into classical chess engine design. The system
models chess positions using quantum registers, enabling superposition-based
piece representation and probabilistic move execution. A quantum-aware minimax
algorithm is employed to explore decision-making under uncertainty, with board
evaluation performed via simulated quantum measurement.

Rather than aiming for competitive performance, this project serves as a
research-oriented prototype to study how quantum principles such as
superposition, measurement, and probabilistic outcomes influence strategic
reasoning in adversarial games. The architecture is designed for extensibility,
making it suitable for experimentation, education, and future research into
hybrid quantum–classical AI systems.

**Quantum Chess Ultimate** is an experimental Python-based project that explores the fusion of **quantum computing concepts** with **chess engine design**.  
It reimagines classical chess by introducing **quantum superposition, probabilistic moves, and quantum-aware decision-making** using IBM’s Qiskit framework.

This project is intended for **learning, experimentation, and research**, rather than competitive play (for now).

---

## 🚀 Project Vision

Traditional chess engines operate on deterministic board states.  
Quantum Chess Ultimate challenges this assumption by allowing:

- Pieces to exist in **superposition**
- Moves that create **probabilistic outcomes**
- Board evaluations that depend on **quantum measurements**
- Search algorithms that are **quantum-aware**

This makes the engine fundamentally different from classical chess AIs like Stockfish.

---

## 🧠 What Makes Quantum Chess Different?

In **quantum chess**:

- A piece may occupy **multiple squares simultaneously**
- Captures are **probabilistic**
- Measuring the board collapses quantum states into classical outcomes
- Strategy involves managing **uncertainty and interference**

This engine models those ideas at a **conceptual and computational level**, not as a full physical quantum system.

---

## 🧩 Core Concepts Implemented

### 1. Quantum Board Representation
- Each square uses **5 qubits**:
  - `3 qubits` → piece type (pawn, knight, bishop, etc.)
  - `1 qubit` → piece color (white / black)
  - `1 qubit` → superposition state
- Allows classical and quantum positions to coexist

---

### 2. Quantum Move Generation
- Moves are implemented as **quantum circuits**
- Uses:
  - `RY` rotations to control superposition probability
  - `CSWAP` (controlled swap) gates to move piece data
- Supports probabilistic positioning instead of fixed movement

---

### 3. Position Evaluation
- Evaluates:
  - Classical piece values
  - Positional advantages (e.g., pawn advancement)
  - Quantum properties like superposition
- Superposed pieces are weighted higher due to tactical potential

---

### 4. Quantum Minimax Search
- Modified **minimax with alpha-beta pruning**
- Handles:
  - Quantum uncertainty
  - Measurement-based evaluation
  - Recursive exploration of probabilistic states

---

## 🧪 Engine Implementation (Core File)

The core logic of **Quantum Chess Ultimate** is implemented in:

quantum-chess-engine.py

This file defines the `QuantumChessEngine` class, which encapsulates the full lifecycle of a quantum chess position—from representation and move generation to evaluation and decision-making.

---

### 🔧 Architectural Overview

The engine is organized around five conceptual layers:

#### 1. Quantum Board Abstraction
- Each chess square is mapped to a **5-qubit quantum register**
- Qubit layout per square:
  - 3 qubits → piece identity
  - 1 qubit → piece color
  - 1 qubit → superposition control
- This design allows classical positions and quantum uncertainty to coexist in a unified representation

#### 2. Quantum Move Encoding
- Moves are represented as **quantum circuits**
- Superposition is introduced using parameterized `RY` rotations
- Piece transfer between squares is performed using `CSWAP` gates
- This enables a single move to encode multiple probabilistic outcomes

#### 3. Measurement & State Collapse
- Board evaluation requires **measurement of quantum states**
- Each square is measured independently using the QASM simulator
- Measurements collapse quantum states into classical bitstrings used for evaluation

#### 4. Quantum-Aware Evaluation Function
- Assigns values based on:
  - Classical material balance
  - Positional heuristics (e.g., pawn advancement)
  - Quantum properties such as superposition
- Superposed pieces receive higher weights to reflect tactical uncertainty

#### 5. Quantum Minimax Search
- Modified minimax algorithm with alpha–beta pruning
- Handles probabilistic outcomes caused by measurement
- Recursively explores move sequences represented as quantum circuits
- Designed to balance exploration depth with quantum evaluation cost

---

### 🏗️ System Architecture Diagram

Figure: High-level architecture of the Quantum Chess Engine showing data flow between quantum board representation, move generation, evaluation, and search.

```mermaid
flowchart TD
    A[QuantumChessEngine] --> B[Quantum Board]
    A --> C[Move Generator]
    A --> D[Quantum Minimax Search]
    D --> E[Evaluation Function]
    E --> F[Board Measurement]

    B --> B1[Quantum Registers<br/>5 Qubits per Square]
    C --> C1[Quantum Circuits]
    C1 --> C2[RY Rotations]
    C1 --> C3[CSWAP Gates]

    F --> G[QASM Simulator]
    G --> E


### ✅ Why this matters
- Makes the project **instantly understandable**
- Huge plus for reviewers, professors, and contributors
- Zero maintenance cost

---

# 2️⃣ Method-Level Documentation Table

This bridges the gap between **conceptual design** and **actual code**.

### 🔧 Add this section after *Engine Implementation (Core File)*

### 📚 Method-Level Documentation

| Method | Purpose | Key Concepts |
|------|--------|-------------|
| `__init__` | Initializes engine state and simulator | Search depth, QASM backend |
| `_initialize_quantum_board` | Creates quantum registers for all board squares | Qubit encoding, board abstraction |
| `create_move_circuit` | Encodes a chess move as a quantum circuit | Superposition, CSWAP, RY gates |
| `evaluate_position` | Scores a measured board position | Material, position, superposition |
| `quantum_minimax` | Searches best move using quantum-aware minimax | Alpha-beta pruning, recursion |
| `find_best_move` | Returns best move for current state | Decision extraction |
| `_measure_board` | Collapses quantum states to classical bits | Measurement, state collapse |
| `_generate_legal_moves` | Generates candidate quantum moves | Placeholder abstraction |
| `_is_legal_move` | Validates move legality | Classical + quantum rules (future) |

### ⚠️ Design Notes & Limitations

- Legal move generation currently acts as a **placeholder abstraction**
- Entanglement rules are conceptual and not yet physically modeled
- Each board measurement collapses the quantum state (no partial reuse yet)
- Performance is constrained by simulator execution cost

---

### 🎯 Design Philosophy

Rather than simulating a physically perfect quantum system, this engine focuses on:
- **Conceptual correctness**
- **Explorability of quantum decision-making**
- **Extensibility for research and experimentation**

This makes the implementation suitable as:
- A research prototype
- A teaching tool
- A foundation for future quantum game AI systems

(See the complete implementation in the source file for detailed method definitions and inline documentation.)

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Qiskit**
- **NumPy**
- **Quantum Circuit Simulation (QASM Simulator)**

---

## 📦 Installation

```bash
pip install qiskit numpy

▶️ Basic Usage

from quantum_chess_engine import QuantumChessEngine

engine = QuantumChessEngine(depth=3)
best_move = engine.find_best_move()

print(best_move)

⚠️ Note: This project uses a simulator backend and is computationally expensive.

🚧 Current Limitations

Legal move checking is simplified

No GUI or visualization yet

Entanglement rules are conceptual placeholders

Performance is not optimized for large depths

🧭 Future Enhancements

Planned improvements include:

Advanced quantum interference rules

True entanglement between pieces

Circuit optimization for lower gate depth

Machine learning–based evaluation

Parallel quantum search strategies

GUI or web-based visualization

🎓 Who Is This For?

Quantum computing learners

Chess engine developers

AI researchers

Students exploring hybrid AI systems

Anyone curious about “What if chess were quantum?”

📜 Disclaimer

This project is experimental and educational.
It does not represent a physically accurate quantum chess implementation, but rather a computational and conceptual model.

---

## 🗺️ Project Roadmap

This roadmap outlines the planned evolution of **Quantum Chess Ultimate**, from a conceptual prototype to a research-grade quantum AI system.

---

### 📌 Phase 1 — Foundation (Completed ✅)
**Goal:** Establish core quantum chess mechanics

- [x] Quantum board representation using qubits
- [x] Superposition-based move modeling
- [x] Quantum circuit generation for moves
- [x] Basic position evaluation
- [x] Quantum-aware minimax search
- [x] Simulator-based execution (QASM)

---

### 🔬 Phase 2 — Quantum Rules & Accuracy (In Progress 🚧)
**Goal:** Improve realism and rule correctness

- [ ] Formal quantum chess rule set
- [ ] Quantum capture mechanics
- [ ] Partial measurement handling
- [ ] Interference-based move outcomes
- [ ] Improved legality checking
- [ ] Entanglement between pieces

---

### ⚙️ Phase 3 — Performance & Optimization
**Goal:** Make the engine scalable and efficient

- [ ] Circuit depth optimization
- [ ] Gate reduction strategies
- [ ] Caching quantum evaluations
- [ ] Parallel simulation of branches
- [ ] Smarter pruning heuristics

---

### 🧠 Phase 4 — AI & Learning
**Goal:** Add adaptive intelligence

- [ ] Machine learning–based evaluation
- [ ] Training on simulated quantum games
- [ ] Reinforcement learning integration
- [ ] Strategy evolution over time

---

### 🎨 Phase 5 — Visualization & UX
**Goal:** Make the engine observable and interactive

- [ ] Board visualization
- [ ] Quantum state probability display
- [ ] Move tree visualization
- [ ] CLI interface
- [ ] Web or GUI frontend (future)

---

### 📚 Phase 6 — Research & Publication
**Goal:** Academic and open research impact

- [ ] Benchmark against classical engines
- [ ] Publish design notes / whitepaper
- [ ] Experiment with real quantum hardware
- [ ] Educational demos for quantum learning
- [ ] Community-driven research extensions

---

### 🚀 Long-Term Vision
To explore how **uncertainty, probability, and quantum mechanics** can redefine decision-making in strategic games—and inspire new forms of AI beyond classical computation.

🤝 Contributions

Contributions, ideas, and discussions are welcome!
Feel free to fork, experiment, and open pull requests.

📄 License

MIT License (recommended – add a LICENSE file if needed)

⭐ Final Thoughts

Quantum Chess Ultimate explores how uncertainty, probability, and quantum mechanics can reshape classical game AI.
It’s less about winning — and more about rethinking strategy itself.
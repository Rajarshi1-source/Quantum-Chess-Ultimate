# Quantum Chess Ultimate — Experiments

This document describes recommended experiments for evaluating
and extending the Quantum Chess Ultimate engine.

---

## 1. Experimental Goals

- Study decision-making under quantum uncertainty
- Evaluate impact of superposition on move selection
- Measure computational tradeoffs

---

## 2. Baseline Experiments

### 2.1 Deterministic vs Quantum Moves
- Disable superposition (probability = 0)
- Compare against superposition-enabled runs
- Measure evaluation variance

---

### 2.2 Superposition Probability Sweep
- Vary probability from 0.1 → 0.9
- Observe move diversity
- Track evaluation instability

---

### 2.3 Search Depth Scaling
- Depth = 1, 2, 3, 4
- Measure:
  - Runtime
  - Evaluation variance
  - Move consistency

---

## 3. Evaluation Metrics

| Metric | Description |
|-----|------------|
| Score variance | Quantum uncertainty |
| Runtime | Scalability |
| Move diversity | Strategic exploration |
| Collapse sensitivity | Measurement impact |

---

## 4. Reproducibility Notes

- Use fixed random seeds where possible
- Record simulator backend version
- Log measurement outcomes

---

## 5. Future Experiments

- Entangled piece evaluation
- Hybrid classical/quantum comparison
- Hardware vs simulator runs
- Learning-based evaluation benchmarking

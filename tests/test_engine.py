from quantum_chess_engine import QuantumChessEngine

def test_engine_initialization():
    engine = QuantumChessEngine(depth=2)
    assert engine.search_depth == 2
    assert engine.quantum_board is not None

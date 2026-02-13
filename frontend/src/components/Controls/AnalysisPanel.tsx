/* ─── Analysis Panel (Right Sidebar) ─── */
import { useGameStore } from '../../store/gameStore';
import { quantumApi } from '../../services/api';
import { useState } from 'react';
import type { QuantumEvaluation } from '../../types/game';

/* Piece symbols for captured display */
const CAPTURE_SYMBOLS: Record<string, string> = {
    pawn: '♟', knight: '♞', bishop: '♝',
    rook: '♜', queen: '♛', king: '♚',
};

export default function AnalysisPanel() {
    const { gameState, gameId, findBestMove, lastMoveResult } = useGameStore();
    const [evaluation, setEvaluation] = useState<QuantumEvaluation | null>(null);
    const [bestMove, setBestMove] = useState<string | null>(null);
    const [isEvaluating, setIsEvaluating] = useState(false);

    if (!gameState) return null;

    const handleEvaluate = async () => {
        if (!gameId) return;
        setIsEvaluating(true);
        try {
            const { data } = await quantumApi.evaluate(gameId);
            setEvaluation(data);
        } catch { /* ignore */ }
        setIsEvaluating(false);
    };

    const handleBestMove = async () => {
        const move = await findBestMove();
        setBestMove(move);
    };

    const evalPercent = evaluation
        ? Math.max(5, Math.min(95, 50 + evaluation.combined_score * 5))
        : 50;

    return (
        <div className="sidebar">
            <h3>Analysis</h3>

            {/* Status */}
            <div className="q-card">
                <div className="q-card-title">Status</div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <span className={`status-badge status-${gameState.status}`}>
                        {gameState.status}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                        {gameState.turn === 'white' ? '○' : '●'} {gameState.turn}'s turn
                    </span>
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                    Move {gameState.move_count} · {gameState.measurement_count} measurements
                </div>
            </div>

            {/* Evaluation */}
            <div className="q-card">
                <div className="q-card-title">Evaluation</div>
                <div className="eval-bar">
                    <div className="eval-fill" style={{ width: `${evalPercent}%` }} />
                </div>
                {evaluation && (
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                        <div>Classical: <span style={{ color: 'var(--quantum-cyan)' }}>{evaluation.classical_score}</span></div>
                        <div>Quantum: <span style={{ color: 'var(--quantum-magenta)' }}>{evaluation.quantum_score}</span></div>
                        <div>Combined: <span style={{ color: 'var(--quantum-green)', fontWeight: 600 }}>{evaluation.combined_score}</span></div>
                    </div>
                )}
                <div className="controls-row" style={{ marginTop: '0.5rem' }}>
                    <button className="q-btn" onClick={handleEvaluate} disabled={isEvaluating} style={{ flex: 1, fontSize: '0.6rem' }}>
                        {isEvaluating ? '⟳ Analyzing…' : '◎ Evaluate'}
                    </button>
                    <button className="q-btn" onClick={handleBestMove} style={{ flex: 1, fontSize: '0.6rem' }}>
                        ★ Best Move
                    </button>
                </div>
                {bestMove && (
                    <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--quantum-green)' }}>
                        Best: <strong>{bestMove}</strong>
                    </div>
                )}
            </div>

            {/* Captured Pieces */}
            <div className="q-card">
                <div className="q-card-title">Captured</div>
                <div style={{ marginBottom: '0.25rem' }}>
                    <span style={{ fontSize: '0.6rem', color: 'var(--text-muted)' }}>White captured:</span>
                    <div className="captured-pieces">
                        {gameState.captured_pieces.white.map((p, i) => (
                            <span key={i}>{CAPTURE_SYMBOLS[p] || p}</span>
                        ))}
                        {gameState.captured_pieces.white.length === 0 && (
                            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>—</span>
                        )}
                    </div>
                </div>
                <div>
                    <span style={{ fontSize: '0.6rem', color: 'var(--text-muted)' }}>Black captured:</span>
                    <div className="captured-pieces">
                        {gameState.captured_pieces.black.map((p, i) => (
                            <span key={i}>{CAPTURE_SYMBOLS[p] || p}</span>
                        ))}
                        {gameState.captured_pieces.black.length === 0 && (
                            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>—</span>
                        )}
                    </div>
                </div>
            </div>

            {/* Move History */}
            <div className="q-card">
                <div className="q-card-title">Move History</div>
                <div className="move-list">
                    {gameState.move_history.length === 0 && (
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textAlign: 'center', padding: '1rem 0' }}>
                            No moves yet
                        </div>
                    )}
                    {gameState.move_history.map((m, i) => (
                        <div key={i} className="move-entry">
                            <span className="move-number">{m.move_number}.</span>
                            <span className="move-notation">
                                {m.piece === 'pawn' ? '' : m.piece[0].toUpperCase()}
                                {m.from}→{m.to}
                            </span>
                            {m.captured && <span style={{ color: 'var(--quantum-orange)' }}>×{m.captured}</span>}
                            {m.quantum_event && <span className="move-quantum">⚛</span>}
                        </div>
                    ))}
                </div>
            </div>

            {/* Quantum Event */}
            {lastMoveResult?.quantum_event && (
                <div className="q-card" style={{ borderColor: 'var(--quantum-magenta)' }}>
                    <div className="q-card-title" style={{ color: 'var(--quantum-magenta)' }}>Quantum Event</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--quantum-cyan)' }}>
                        {lastMoveResult.quantum_event}
                    </div>
                </div>
            )}
        </div>
    );
}

/* ─── Quantum Controls (Left Sidebar) ─── */
import { useGameStore } from '../../store/gameStore';
import { quantumApi } from '../../services/api';
import { useState, useEffect } from 'react';

interface CircuitStats {
    total_qubits: number;
    circuit_depth: number;
    gate_count: number;
    superposition_count: number;
    entanglement_count: number;
    optimization_suggestions: string[];
}

export default function QuantumControls() {
    const { gameState, gameId } = useGameStore();
    const [circuit, setCircuit] = useState<CircuitStats | null>(null);
    const [isMeasuring, setIsMeasuring] = useState(false);

    const fetchCircuit = async () => {
        if (!gameId) return;
        try {
            const { data } = await quantumApi.getCircuit(gameId);
            setCircuit(data);
        } catch { /* ignore */ }
    };

    useEffect(() => {
        if (gameId) fetchCircuit();
    }, [gameId, gameState?.measurement_count]);

    const handleMeasureAll = async () => {
        if (!gameId) return;
        setIsMeasuring(true);
        try {
            await quantumApi.measure(gameId);
            // Refresh state
            useGameStore.getState().fetchState();
            fetchCircuit();
        } catch { /* ignore */ }
        setIsMeasuring(false);
    };

    if (!gameState) return null;

    const superpositions = gameState.superposition_squares || [];
    const entanglements = gameState.entanglement_pairs || [];

    return (
        <div className="sidebar">
            <h3>Quantum State</h3>

            {/* Stats */}
            <div className="q-card">
                <div className="q-card-title">Quantum Metrics</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.7rem' }}>
                    <div>
                        <div style={{ color: 'var(--text-muted)', fontSize: '0.6rem' }}>Superpositions</div>
                        <div style={{ color: 'var(--quantum-cyan)', fontWeight: 600, fontSize: '1.2rem' }}>
                            {superpositions.length}
                        </div>
                    </div>
                    <div>
                        <div style={{ color: 'var(--text-muted)', fontSize: '0.6rem' }}>Entanglements</div>
                        <div style={{ color: 'var(--quantum-magenta)', fontWeight: 600, fontSize: '1.2rem' }}>
                            {entanglements.length}
                        </div>
                    </div>
                    <div>
                        <div style={{ color: 'var(--text-muted)', fontSize: '0.6rem' }}>Measurements</div>
                        <div style={{ color: 'var(--quantum-green)', fontWeight: 600, fontSize: '1.2rem' }}>
                            {gameState.measurement_count}
                        </div>
                    </div>
                    <div>
                        <div style={{ color: 'var(--text-muted)', fontSize: '0.6rem' }}>Q-Probability</div>
                        <div style={{ color: 'var(--quantum-orange)', fontWeight: 600, fontSize: '1.2rem' }}>
                            {Math.round(gameState.quantum_probability * 100)}%
                        </div>
                    </div>
                </div>
            </div>

            {/* Circuit info */}
            {circuit && (
                <div className="q-card">
                    <div className="q-card-title">Circuit</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span>Qubits:</span>
                            <span style={{ color: 'var(--quantum-cyan)' }}>{circuit.total_qubits}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span>Depth:</span>
                            <span style={{ color: 'var(--quantum-cyan)' }}>{circuit.circuit_depth}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span>Gates:</span>
                            <span style={{ color: 'var(--quantum-cyan)' }}>{circuit.gate_count}</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Superposition list */}
            {superpositions.length > 0 && (
                <div className="q-card">
                    <div className="q-card-title">Active Superpositions</div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem' }}>
                        {superpositions.map((sq) => (
                            <span
                                key={sq}
                                style={{
                                    fontSize: '0.7rem',
                                    padding: '0.2rem 0.4rem',
                                    background: 'rgba(0, 240, 255, 0.1)',
                                    border: '1px solid var(--quantum-cyan)',
                                    borderRadius: '4px',
                                    color: 'var(--quantum-cyan)',
                                }}
                            >
                                {sq}
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Entanglement list */}
            {entanglements.length > 0 && (
                <div className="q-card">
                    <div className="q-card-title">Entangled Pairs</div>
                    <div style={{ fontSize: '0.7rem' }}>
                        {entanglements.map(([a, b], i) => (
                            <div key={i} style={{ color: 'var(--quantum-magenta)', marginBottom: '0.2rem' }}>
                                {a} ⟺ {b}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Measurement button */}
            <div className="q-card">
                <div className="q-card-title">Actions</div>
                <button
                    className="q-btn"
                    onClick={handleMeasureAll}
                    disabled={isMeasuring || superpositions.length === 0}
                    style={{ width: '100%', fontSize: '0.65rem' }}
                >
                    {isMeasuring ? '⟳ Measuring…' : `◉ Measure All (${superpositions.length})`}
                </button>
                {superpositions.length === 0 && (
                    <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: '0.25rem', textAlign: 'center' }}>
                        No active superpositions
                    </div>
                )}
            </div>

            {/* Mode indicator */}
            <div className="q-card" style={{ textAlign: 'center' }}>
                <div style={{
                    fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.15em',
                    color: gameState.mode === 'quantum' ? 'var(--quantum-cyan)' :
                        gameState.mode === 'hybrid' ? 'var(--quantum-magenta)' : 'var(--text-muted)',
                }}>
                    {gameState.mode} Mode
                </div>
            </div>
        </div>
    );
}

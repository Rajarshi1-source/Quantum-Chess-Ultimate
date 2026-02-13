/* ─── Game Controls Component ─── */
import { useGameStore } from '../../store/gameStore';
import { useUIStore } from '../../store/uiStore';
import type { GameMode } from '../../types/game';
import { useState } from 'react';

export default function GameControls() {
    const { gameId, gameState, createGame, reset, isLoading } = useGameStore();
    const { toggleQuantumOverlay, showQuantumOverlay, flipBoard } = useUIStore();
    const [selectedMode, setSelectedMode] = useState<GameMode>('quantum');

    const handleNewGame = () => {
        createGame({
            mode: selectedMode,
            quantum_probability: 0.5,
            search_depth: 3,
        });
    };

    return (
        <div>
            <div className="q-card">
                <div className="q-card-title">Game Controls</div>

                {/* Mode selector */}
                <div style={{ marginBottom: '0.75rem' }}>
                    <label style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.25rem' }}>
                        Mode
                    </label>
                    <select
                        value={selectedMode}
                        onChange={(e) => setSelectedMode(e.target.value as GameMode)}
                        style={{
                            width: '100%',
                            padding: '0.4rem',
                            background: 'var(--bg-secondary)',
                            border: '1px solid var(--border-color)',
                            borderRadius: '4px',
                            color: 'var(--text-primary)',
                            fontFamily: 'JetBrains Mono',
                            fontSize: '0.75rem',
                        }}
                    >
                        <option value="quantum">⚛ Quantum</option>
                        <option value="classical">♟ Classical</option>
                        <option value="hybrid">⚡ Hybrid</option>
                    </select>
                </div>

                <div className="controls-row">
                    <button
                        className="q-btn q-btn-primary"
                        onClick={handleNewGame}
                        disabled={isLoading}
                        style={{ flex: 1 }}
                    >
                        {gameId ? '↻ New Game' : '▶ Start'}
                    </button>

                    {gameId && (
                        <button className="q-btn q-btn-danger" onClick={reset}>
                            ✕
                        </button>
                    )}
                </div>
            </div>

            {/* View controls */}
            {gameState && (
                <div className="q-card">
                    <div className="q-card-title">View</div>
                    <div className="controls-row">
                        <button
                            className={`q-btn ${showQuantumOverlay ? 'q-btn-primary' : ''}`}
                            onClick={toggleQuantumOverlay}
                            style={{ flex: 1, fontSize: '0.6rem' }}
                        >
                            {showQuantumOverlay ? '⚛ Quantum ON' : '⚛ Quantum OFF'}
                        </button>
                        <button
                            className="q-btn"
                            onClick={flipBoard}
                            style={{ fontSize: '0.6rem' }}
                        >
                            ⇅ Flip
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

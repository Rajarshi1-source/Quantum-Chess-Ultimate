/* ─── Quantum Chess Ultimate — Main App ─── */
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ChessBoard from './components/Board/ChessBoard';
import GameControls from './components/Controls/GameControls';
import QuantumControls from './components/Controls/QuantumControls';
import AnalysisPanel from './components/Controls/AnalysisPanel';
import { useGameStore } from './store/gameStore';

export default function App() {
  const { gameState, isLoading, error, lastMoveResult } = useGameStore();
  const [toast, setToast] = useState<string | null>(null);

  /* Show quantum event toasts */
  useEffect(() => {
    if (lastMoveResult?.quantum_event) {
      setToast(lastMoveResult.quantum_event);
      const timer = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [lastMoveResult]);

  return (
    <>
      {/* Animated background */}
      <div className="quantum-bg" />

      <div className="app-container scan-lines">
        {/* ─── Header ─── */}
        <header className="app-header">
          <h1>Quantum Chess</h1>

          {gameState && (
            <div className="header-stats">
              <span>
                Mode:<span className="stat-value">{gameState.mode}</span>
              </span>
              <span>
                Turn:<span className="stat-value">{gameState.turn === 'white' ? '○ White' : '● Black'}</span>
              </span>
              <span>
                Moves:<span className="stat-value">{gameState.move_count}</span>
              </span>
              <span>
                ⚛ Superpositions:<span className="stat-value">{gameState.superposition_squares?.length ?? 0}</span>
              </span>
            </div>
          )}

          {!gameState && (
            <div className="header-stats">
              <span style={{ color: 'var(--text-muted)' }}>
                Create a game to begin
              </span>
            </div>
          )}
        </header>

        {/* ─── Main Content ─── */}
        <main className="app-main">
          {/* Left sidebar: Quantum controls + Game controls */}
          <div>
            <GameControls />
            {gameState && <QuantumControls />}
          </div>

          {/* Center: Chess board */}
          <ChessBoard />

          {/* Right sidebar: Analysis */}
          {gameState ? (
            <AnalysisPanel />
          ) : (
            <div className="sidebar" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
              <div>
                <div style={{ fontSize: '2.5rem', marginBottom: '1rem', opacity: 0.3 }}>⚛</div>
                <div style={{ fontFamily: 'Orbitron', fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                  Quantum Chess Ultimate
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
                  Experience chess with quantum mechanics.
                  Pieces can exist in superposition,
                  become entangled, and require
                  measurement to collapse.
                </div>
              </div>
            </div>
          )}
        </main>

        {/* ─── Error display ─── */}
        {error && (
          <div style={{
            position: 'fixed', bottom: '4rem', left: '50%', transform: 'translateX(-50%)',
            background: 'rgba(255, 51, 102, 0.15)', border: '1px solid #ff3366',
            borderRadius: '8px', padding: '0.5rem 1rem', fontSize: '0.75rem', color: '#ff3366',
            zIndex: 200,
          }}>
            {error}
          </div>
        )}

        {/* ─── Quantum event toast ─── */}
        <AnimatePresence>
          {toast && (
            <motion.div
              className="quantum-toast"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 30 }}
            >
              ⚛ {toast}
            </motion.div>
          )}
        </AnimatePresence>

        {/* ─── Loading overlay ─── */}
        {isLoading && (
          <div className="loading-overlay">
            <div className="quantum-spinner" />
          </div>
        )}
      </div>
    </>
  );
}

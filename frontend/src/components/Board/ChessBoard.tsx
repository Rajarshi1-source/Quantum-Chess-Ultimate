/* ─── Chess Board Component ─── */
import { useGameStore } from '../../store/gameStore';
import { useUIStore } from '../../store/uiStore';
import Piece from './Piece';
import type { PieceInfo } from '../../types/game';

const FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
const RANKS = ['8', '7', '6', '5', '4', '3', '2', '1'];

export default function ChessBoard() {
    const {
        gameState, selectedSquare, legalMoves,
        selectSquare, lastMoveResult,
    } = useGameStore();
    const { boardFlipped, showQuantumOverlay } = useUIStore();

    const files = boardFlipped ? [...FILES].reverse() : FILES;
    const ranks = boardFlipped ? [...RANKS].reverse() : RANKS;

    const isSquareLight = (file: string, rank: string) => {
        const f = FILES.indexOf(file);
        const r = RANKS.indexOf(rank);
        return (f + r) % 2 === 0;
    };

    const getSquareClasses = (square: string, piece: PieceInfo | undefined) => {
        const file = square[0];
        const rank = square[1];
        const classes: string[] = ['square'];

        classes.push(isSquareLight(file, rank) ? 'square-light' : 'square-dark');

        if (selectedSquare === square) {
            classes.push('square-selected');
        }

        if (legalMoves.includes(square)) {
            classes.push(piece ? 'square-legal-capture' : 'square-legal');
        }

        // Highlight last move
        if (lastMoveResult?.success) {
            if (square === lastMoveResult.from_square || square === lastMoveResult.to_square) {
                classes.push('square-last-move');
            }
        }

        // Check highlight
        if (gameState && (gameState.status === 'check' || gameState.status === 'checkmate')) {
            if (piece?.type === 'king' && piece.color === gameState.turn) {
                classes.push('square-check');
            }
        }

        return classes.join(' ');
    };

    if (!gameState) {
        return (
            <div className="board-container">
                <div style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                    <p style={{ fontFamily: 'Orbitron', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
                        No active game
                    </p>
                    <p style={{ fontSize: '0.75rem' }}>Create a new game to begin</p>
                </div>
            </div>
        );
    }

    return (
        <div className="board-container">
            <div className="board-wrapper">
                {/* Rank labels */}
                <div className="board-ranks">
                    {ranks.map((r) => <span key={r}>{r}</span>)}
                </div>

                {/* Board grid */}
                <div>
                    <div className="chess-board">
                        {ranks.map((rank) =>
                            files.map((file) => {
                                const square = `${file}${rank}`;
                                const piece = gameState.position[square];
                                const isInSuperposition = gameState.superposition_squares?.includes(square);

                                return (
                                    <div
                                        key={square}
                                        className={getSquareClasses(square, piece)}
                                        onClick={() => selectSquare(square)}
                                        data-square={square}
                                    >
                                        {piece && (
                                            <Piece
                                                type={piece.type}
                                                color={piece.color}
                                                inSuperposition={piece.in_superposition || isInSuperposition}
                                                probability={piece.superposition_probability}
                                            />
                                        )}

                                        {/* Quantum overlay */}
                                        {showQuantumOverlay && isInSuperposition && (
                                            <div className="superposition-overlay" />
                                        )}

                                        {/* Probability badge */}
                                        {showQuantumOverlay && piece?.in_superposition && (
                                            <span className="probability-badge">
                                                {Math.round((piece.superposition_probability ?? 1) * 100)}%
                                            </span>
                                        )}
                                    </div>
                                );
                            })
                        )}
                    </div>

                    {/* File labels */}
                    <div className="board-files">
                        {files.map((f) => <span key={f}>{f}</span>)}
                    </div>
                </div>
            </div>
        </div>
    );
}

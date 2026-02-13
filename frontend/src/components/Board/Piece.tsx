/* ─── Chess Piece Component ─── */
import type { PieceType, PieceColor } from '../../types/game';

/* Unicode chess pieces */
const PIECE_SYMBOLS: Record<PieceColor, Record<PieceType, string>> = {
    white: {
        king: '♔', queen: '♕', rook: '♖',
        bishop: '♗', knight: '♘', pawn: '♙',
    },
    black: {
        king: '♚', queen: '♛', rook: '♜',
        bishop: '♝', knight: '♞', pawn: '♟',
    },
};

interface PieceProps {
    type: PieceType;
    color: PieceColor;
    inSuperposition?: boolean;
    probability?: number;
}

export default function Piece({ type, color, inSuperposition, probability }: PieceProps) {
    const symbol = PIECE_SYMBOLS[color]?.[type] ?? '';
    const classes = [
        'piece',
        `piece-${color}`,
        inSuperposition ? 'piece-superposition' : '',
    ].filter(Boolean).join(' ');

    return (
        <span className={classes} title={`${color} ${type}${probability != null ? ` (${Math.round(probability * 100)}%)` : ''}`}>
            {symbol}
        </span>
    );
}

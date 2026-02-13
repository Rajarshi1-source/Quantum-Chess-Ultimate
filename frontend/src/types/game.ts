/* ─── TypeScript Types for Quantum Chess ─── */

/* Enums */
export type GameMode = 'classical' | 'quantum' | 'hybrid' | 'tutorial';
export type PieceColor = 'white' | 'black';
export type PieceType = 'pawn' | 'knight' | 'bishop' | 'rook' | 'queen' | 'king';
export type GameStatus = 'active' | 'check' | 'checkmate' | 'stalemate' | 'draw' | 'resigned';

/* Piece */
export interface PieceInfo {
    type: PieceType;
    color: PieceColor;
    in_superposition: boolean;
    superposition_probability: number;
}

/* Game Config */
export interface GameConfig {
    mode: GameMode;
    quantum_probability: number;
    search_depth: number;
    player_white: string;
    player_black: string;
}

/* Game State */
export interface GameState {
    game_id: string;
    mode: GameMode;
    status: GameStatus;
    turn: PieceColor;
    position: Record<string, PieceInfo>;
    move_count: number;
    measurement_count: number;
    quantum_probability: number;
    superposition_squares: string[];
    entanglement_pairs: [string, string][];
    move_history: MoveHistoryEntry[];
    captured_pieces: { white: string[]; black: string[] };
    created_at: string;
    updated_at: string;
}

/* Move */
export interface Move {
    from_square: string;
    to_square: string;
    promotion?: string;
}

export interface MoveResult {
    success: boolean;
    from_square: string;
    to_square: string;
    piece_moved: string;
    piece_captured: string | null;
    is_check: boolean;
    is_checkmate: boolean;
    is_stalemate: boolean;
    quantum_event: string | null;
    quantum_probability: number | null;
    superposition_created: boolean;
    measurement_triggered: boolean;
    message: string;
}

export interface MoveHistoryEntry {
    move_number: number;
    from: string;
    to: string;
    piece: string;
    color: string;
    captured: string | null;
    quantum_event: string | null;
}

/* Quantum */
export interface QuantumEvaluation {
    game_id: string;
    classical_score: number;
    quantum_score: number;
    combined_score: number;
    uncertainty: number;
    best_move: string | null;
    evaluation_depth: number;
    samples_taken: number;
}

export interface CircuitInfo {
    game_id: string;
    total_qubits: number;
    circuit_depth: number;
    gate_count: number;
    superposition_count: number;
    entanglement_count: number;
}

/* Legal Moves Response */
export interface LegalMovesResponse {
    square: string;
    legal_moves: string[];
    quantum_moves: string[];
}

/* API Responses */
export interface GameCreateResponse {
    game_id: string;
    state: GameState;
    message: string;
}

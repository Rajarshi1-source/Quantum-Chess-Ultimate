/* ─── API Service Layer ─── */
import axios from 'axios';
import type {
    GameConfig, GameState, GameCreateResponse,
    Move, MoveResult, LegalMovesResponse,
    QuantumEvaluation,
} from '../types/game';

const api = axios.create({
    baseURL: '/api',
    headers: { 'Content-Type': 'application/json' },
});

/* Game endpoints */
export const gameApi = {
    create: (config?: Partial<GameConfig>) =>
        api.post<GameCreateResponse>('/game/new', config ?? {}),

    getState: (gameId: string) =>
        api.get<GameState>(`/game/${gameId}`),

    makeMove: (gameId: string, move: Move) =>
        api.post<MoveResult>(`/game/${gameId}/move`, move),

    getLegalMoves: (gameId: string, square: string) =>
        api.get<LegalMovesResponse>(`/game/${gameId}/legal-moves/${square}`),

    getAllLegalMoves: (gameId: string) =>
        api.get<{ game_id: string; moves: Record<string, string[]> }>(
            `/game/${gameId}/all-legal-moves`
        ),

    deleteGame: (gameId: string) =>
        api.delete(`/game/${gameId}`),
};

/* Quantum endpoints */
export const quantumApi = {
    evaluate: (gameId: string) =>
        api.post<QuantumEvaluation>(`/quantum/${gameId}/evaluate`),

    getBestMove: (gameId: string) =>
        api.get<{ game_id: string; best_move: string; score: number }>(
            `/quantum/${gameId}/best-move`
        ),

    measure: (gameId: string, square?: string) =>
        api.post(`/quantum/${gameId}/measure`, { square: square ?? null }),

    getCircuit: (gameId: string) =>
        api.get(`/quantum/${gameId}/circuit`),

    getSuperposition: (gameId: string) =>
        api.get(`/quantum/${gameId}/superposition`),
};

/* Analysis endpoints */
export const analysisApi = {
    analyzePosition: (gameId: string) =>
        api.post(`/analysis/${gameId}/position`),

    getHistory: (gameId: string) =>
        api.get(`/analysis/${gameId}/history`),

    getSquareProbability: (gameId: string, square: string) =>
        api.get(`/analysis/${gameId}/probability/${square}`),
};

export default api;

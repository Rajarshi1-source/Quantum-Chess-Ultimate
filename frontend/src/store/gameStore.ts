/* ─── Zustand Game Store ─── */
import { create } from 'zustand';
import type { GameState, Move, MoveResult, GameConfig } from '../types/game';
import { gameApi, quantumApi } from '../services/api';

interface GameStore {
    /* State */
    gameId: string | null;
    gameState: GameState | null;
    selectedSquare: string | null;
    legalMoves: string[];
    lastMoveResult: MoveResult | null;
    isLoading: boolean;
    error: string | null;

    /* Actions */
    createGame: (config?: Partial<GameConfig>) => Promise<void>;
    makeMove: (move: Move) => Promise<MoveResult | null>;
    selectSquare: (square: string | null) => void;
    fetchLegalMoves: (square: string) => Promise<void>;
    fetchState: () => Promise<void>;
    findBestMove: () => Promise<string | null>;
    reset: () => void;
}

export const useGameStore = create<GameStore>((set, get) => ({
    gameId: null,
    gameState: null,
    selectedSquare: null,
    legalMoves: [],
    lastMoveResult: null,
    isLoading: false,
    error: null,

    createGame: async (config) => {
        set({ isLoading: true, error: null });
        try {
            const { data } = await gameApi.create(config);
            set({
                gameId: data.game_id,
                gameState: data.state,
                selectedSquare: null,
                legalMoves: [],
                lastMoveResult: null,
                isLoading: false,
            });
        } catch (err: any) {
            set({ error: err.message, isLoading: false });
        }
    },

    makeMove: async (move) => {
        const { gameId } = get();
        if (!gameId) return null;

        set({ isLoading: true, error: null });
        try {
            const { data: result } = await gameApi.makeMove(gameId, move);
            if (result.success) {
                const { data: state } = await gameApi.getState(gameId);
                set({
                    gameState: state,
                    selectedSquare: null,
                    legalMoves: [],
                    lastMoveResult: result,
                    isLoading: false,
                });
            } else {
                set({ error: result.message, isLoading: false, lastMoveResult: result });
            }
            return result;
        } catch (err: any) {
            set({ error: err.message, isLoading: false });
            return null;
        }
    },

    selectSquare: (square) => {
        const { gameState, selectedSquare, legalMoves, makeMove } = get();
        if (!gameState) return;

        // If a square is already selected and this is a legal target, make the move
        if (selectedSquare && square && legalMoves.includes(square)) {
            makeMove({ from_square: selectedSquare, to_square: square });
            return;
        }

        // If clicking on own piece, select it
        if (square && gameState.position[square]) {
            const piece = gameState.position[square];
            if (piece.color === gameState.turn) {
                set({ selectedSquare: square });
                get().fetchLegalMoves(square);
                return;
            }
        }

        // Deselect
        set({ selectedSquare: null, legalMoves: [] });
    },

    fetchLegalMoves: async (square) => {
        const { gameId } = get();
        if (!gameId) return;
        try {
            const { data } = await gameApi.getLegalMoves(gameId, square);
            set({ legalMoves: data.legal_moves });
        } catch {
            set({ legalMoves: [] });
        }
    },

    fetchState: async () => {
        const { gameId } = get();
        if (!gameId) return;
        try {
            const { data } = await gameApi.getState(gameId);
            set({ gameState: data });
        } catch (err: any) {
            set({ error: err.message });
        }
    },

    findBestMove: async () => {
        const { gameId } = get();
        if (!gameId) return null;
        try {
            const { data } = await quantumApi.getBestMove(gameId);
            return data.best_move;
        } catch {
            return null;
        }
    },

    reset: () => {
        set({
            gameId: null,
            gameState: null,
            selectedSquare: null,
            legalMoves: [],
            lastMoveResult: null,
            isLoading: false,
            error: null,
        });
    },
}));

/**
 * Quantum Chess Ultimate — Frontend Unit Tests (Vitest)
 *
 * Tests for Zustand stores and utility logic.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';

/* ─── Game Store Tests ──────────────────────────────────────── */

describe('GameStore', () => {
    beforeEach(() => {
        vi.resetModules();
    });

    it('should have correct initial state', async () => {
        const { useGameStore } = await import('../store/gameStore');
        const state = useGameStore.getState();
        expect(state.gameId).toBeNull();
        expect(state.gameState).toBeNull();
        expect(state.selectedSquare).toBeNull();
        expect(state.legalMoves).toEqual([]);
        expect(state.lastMoveResult).toBeNull();
        expect(state.isLoading).toBe(false);
        expect(state.error).toBeNull();
    });

    it('should reset state correctly', async () => {
        const { useGameStore } = await import('../store/gameStore');
        // Manually set some state
        useGameStore.setState({
            gameId: 'test-123',
            error: 'some error',
            isLoading: true,
        });

        useGameStore.getState().reset();
        const state = useGameStore.getState();
        expect(state.gameId).toBeNull();
        expect(state.error).toBeNull();
        expect(state.isLoading).toBe(false);
    });

    it('should handle selectSquare with no active game', async () => {
        const { useGameStore } = await import('../store/gameStore');
        // Should not throw when no game exists
        useGameStore.getState().selectSquare('e2');
        expect(useGameStore.getState().selectedSquare).toBeNull();
    });
});

/* ─── UI Store Tests ────────────────────────────────────────── */

describe('UIStore', () => {
    beforeEach(() => {
        vi.resetModules();
    });

    it('should have correct initial state', async () => {
        const { useUIStore } = await import('../store/uiStore');
        const state = useUIStore.getState();
        expect(state.showQuantumOverlay).toBe(true);
        expect(state.showAnalysisPanel).toBe(true);
        expect(state.theme).toBe('dark');
        expect(state.boardFlipped).toBe(false);
    });

    it('should toggle quantum overlay', async () => {
        const { useUIStore } = await import('../store/uiStore');
        expect(useUIStore.getState().showQuantumOverlay).toBe(true);
        useUIStore.getState().toggleQuantumOverlay();
        expect(useUIStore.getState().showQuantumOverlay).toBe(false);
        useUIStore.getState().toggleQuantumOverlay();
        expect(useUIStore.getState().showQuantumOverlay).toBe(true);
    });

    it('should toggle theme', async () => {
        const { useUIStore } = await import('../store/uiStore');
        expect(useUIStore.getState().theme).toBe('dark');
        useUIStore.getState().toggleTheme();
        expect(useUIStore.getState().theme).toBe('light');
        useUIStore.getState().toggleTheme();
        expect(useUIStore.getState().theme).toBe('dark');
    });

    it('should flip board', async () => {
        const { useUIStore } = await import('../store/uiStore');
        expect(useUIStore.getState().boardFlipped).toBe(false);
        useUIStore.getState().flipBoard();
        expect(useUIStore.getState().boardFlipped).toBe(true);
    });

    it('should toggle analysis panel', async () => {
        const { useUIStore } = await import('../store/uiStore');
        expect(useUIStore.getState().showAnalysisPanel).toBe(true);
        useUIStore.getState().toggleAnalysisPanel();
        expect(useUIStore.getState().showAnalysisPanel).toBe(false);
    });
});

/* ─── Type Validation Tests ─────────────────────────────────── */

describe('Type Definitions', () => {
    it('should export all required types', async () => {
        const types = await import('../types/game');
        // Verify type exports exist (they're just interfaces, so we check the module loaded)
        expect(types).toBeDefined();
    });
});

/* ─── API Service Tests ─────────────────────────────────────── */

describe('API Service', () => {
    it('should export all API modules', async () => {
        const { gameApi, quantumApi, analysisApi } = await import('../services/api');
        expect(gameApi).toBeDefined();
        expect(gameApi.create).toBeTypeOf('function');
        expect(gameApi.makeMove).toBeTypeOf('function');
        expect(gameApi.getLegalMoves).toBeTypeOf('function');
        expect(quantumApi).toBeDefined();
        expect(quantumApi.evaluate).toBeTypeOf('function');
        expect(quantumApi.getBestMove).toBeTypeOf('function');
        expect(analysisApi).toBeDefined();
        expect(analysisApi.analyzePosition).toBeTypeOf('function');
    });
});

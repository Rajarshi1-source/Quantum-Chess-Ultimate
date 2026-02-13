/* ─── Zustand UI Store ─── */
import { create } from 'zustand';

interface UIStore {
    showQuantumOverlay: boolean;
    showAnalysisPanel: boolean;
    theme: 'dark' | 'light';
    boardFlipped: boolean;

    toggleQuantumOverlay: () => void;
    toggleAnalysisPanel: () => void;
    toggleTheme: () => void;
    flipBoard: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
    showQuantumOverlay: true,
    showAnalysisPanel: true,
    theme: 'dark',
    boardFlipped: false,

    toggleQuantumOverlay: () =>
        set((s) => ({ showQuantumOverlay: !s.showQuantumOverlay })),
    toggleAnalysisPanel: () =>
        set((s) => ({ showAnalysisPanel: !s.showAnalysisPanel })),
    toggleTheme: () =>
        set((s) => ({ theme: s.theme === 'dark' ? 'light' : 'dark' })),
    flipBoard: () =>
        set((s) => ({ boardFlipped: !s.boardFlipped })),
}));

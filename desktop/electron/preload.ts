/**
 * Quantum Chess Ultimate — Electron Preload Script
 *
 * Secure bridge between main process and renderer using contextBridge.
 * Exposes a controlled API surface to the renderer process.
 */

import { contextBridge, ipcRenderer } from 'electron';

/** Allowed IPC channels for send/receive */
const SEND_CHANNELS = [
    'game:save',
    'game:load',
    'game:export-pgn',
    'app:check-updates',
] as const;

const RECEIVE_CHANNELS = [
    'menu:new-game',
    'menu:save-game',
    'menu:load-game',
    'menu:export-pgn',
    'menu:undo',
    'menu:redo',
    'menu:flip-board',
    'menu:toggle-quantum',
    'menu:measure-all',
    'menu:ai-move',
    'menu:show-rules',
    'menu:check-updates',
    'game:saved',
    'game:loaded',
    'game:export-complete',
    'updater:status',
] as const;

type SendChannel = typeof SEND_CHANNELS[number];
type ReceiveChannel = typeof RECEIVE_CHANNELS[number];

contextBridge.exposeInMainWorld('quantumChess', {
    /** Send a message to the main process */
    send: (channel: SendChannel, data?: unknown) => {
        if (SEND_CHANNELS.includes(channel)) {
            ipcRenderer.send(channel, data);
        }
    },

    /** Invoke a main-process handler and await the result */
    invoke: (channel: string, ...args: unknown[]) => {
        const allowed = ['game:save', 'game:load', 'game:export-pgn', 'dialog:open', 'dialog:save'];
        if (allowed.includes(channel)) {
            return ipcRenderer.invoke(channel, ...args);
        }
        return Promise.reject(new Error(`Channel "${channel}" not allowed`));
    },

    /** Listen for messages from the main process */
    on: (channel: ReceiveChannel, callback: (...args: unknown[]) => void) => {
        if (RECEIVE_CHANNELS.includes(channel)) {
            const handler = (_event: Electron.IpcRendererEvent, ...args: unknown[]) => callback(...args);
            ipcRenderer.on(channel, handler);
            // Return cleanup function
            return () => ipcRenderer.removeListener(channel, handler);
        }
        return () => { };
    },

    /** One-time listener */
    once: (channel: ReceiveChannel, callback: (...args: unknown[]) => void) => {
        if (RECEIVE_CHANNELS.includes(channel)) {
            ipcRenderer.once(channel, (_event, ...args) => callback(...args));
        }
    },

    /** Platform info */
    platform: process.platform,
    isElectron: true,
});

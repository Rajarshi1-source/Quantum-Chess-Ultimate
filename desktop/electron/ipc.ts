/**
 * Quantum Chess Ultimate — IPC Handlers
 *
 * Handles file system operations for game save/load and PGN export.
 */

import { ipcMain, dialog, BrowserWindow } from 'electron';
import * as fs from 'fs';
import * as path from 'path';
import { app } from 'electron';

/** Default save directory */
const SAVE_DIR = path.join(app.getPath('userData'), 'saves');

function ensureSaveDir(): void {
    if (!fs.existsSync(SAVE_DIR)) {
        fs.mkdirSync(SAVE_DIR, { recursive: true });
    }
}

export function registerIpcHandlers(): void {
    /* ─── Save Game ───────────────────────────────────────── */

    ipcMain.handle('game:save', async (_event, gameData: { id: string; state: object }) => {
        ensureSaveDir();
        try {
            const filename = `quantum-chess-${gameData.id}-${Date.now()}.json`;
            const win = BrowserWindow.getFocusedWindow();
            const result = await dialog.showSaveDialog(win!, {
                title: 'Save Quantum Chess Game',
                defaultPath: path.join(SAVE_DIR, filename),
                filters: [
                    { name: 'Quantum Chess Save', extensions: ['json'] },
                    { name: 'All Files', extensions: ['*'] },
                ],
            });

            if (result.canceled || !result.filePath) {
                return { success: false, message: 'Save cancelled' };
            }

            const saveData = {
                version: '1.0.0',
                savedAt: new Date().toISOString(),
                ...gameData,
            };

            fs.writeFileSync(result.filePath, JSON.stringify(saveData, null, 2), 'utf-8');
            return { success: true, filePath: result.filePath, message: 'Game saved successfully' };
        } catch (err: any) {
            return { success: false, message: `Save failed: ${err.message}` };
        }
    });

    /* ─── Load Game ───────────────────────────────────────── */

    ipcMain.handle('game:load', async () => {
        try {
            const win = BrowserWindow.getFocusedWindow();
            const result = await dialog.showOpenDialog(win!, {
                title: 'Load Quantum Chess Game',
                defaultPath: SAVE_DIR,
                filters: [
                    { name: 'Quantum Chess Save', extensions: ['json'] },
                    { name: 'All Files', extensions: ['*'] },
                ],
                properties: ['openFile'],
            });

            if (result.canceled || result.filePaths.length === 0) {
                return { success: false, message: 'Load cancelled' };
            }

            const raw = fs.readFileSync(result.filePaths[0], 'utf-8');
            const data = JSON.parse(raw);

            if (!data.version || !data.state) {
                return { success: false, message: 'Invalid save file format' };
            }

            return { success: true, data, message: 'Game loaded successfully' };
        } catch (err: any) {
            return { success: false, message: `Load failed: ${err.message}` };
        }
    });

    /* ─── Export PGN ──────────────────────────────────────── */

    ipcMain.handle('game:export-pgn', async (_event, pgnContent: string) => {
        try {
            const win = BrowserWindow.getFocusedWindow();
            const result = await dialog.showSaveDialog(win!, {
                title: 'Export as PGN',
                defaultPath: path.join(app.getPath('documents'), `quantum-chess-${Date.now()}.pgn`),
                filters: [
                    { name: 'PGN File', extensions: ['pgn'] },
                    { name: 'Text File', extensions: ['txt'] },
                ],
            });

            if (result.canceled || !result.filePath) {
                return { success: false, message: 'Export cancelled' };
            }

            fs.writeFileSync(result.filePath, pgnContent, 'utf-8');
            return { success: true, filePath: result.filePath, message: 'PGN exported successfully' };
        } catch (err: any) {
            return { success: false, message: `Export failed: ${err.message}` };
        }
    });

    /* ─── Dialog helpers ──────────────────────────────────── */

    ipcMain.handle('dialog:open', async (_event, options: Electron.OpenDialogOptions) => {
        const win = BrowserWindow.getFocusedWindow();
        return dialog.showOpenDialog(win!, options);
    });

    ipcMain.handle('dialog:save', async (_event, options: Electron.SaveDialogOptions) => {
        const win = BrowserWindow.getFocusedWindow();
        return dialog.showSaveDialog(win!, options);
    });
}

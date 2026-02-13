/**
 * Quantum Chess Ultimate — Auto-Updater
 *
 * Uses electron-updater to check for and apply updates automatically.
 */

import { autoUpdater } from 'electron-updater';
import { BrowserWindow } from 'electron';

export function setupAutoUpdater(mainWindow: BrowserWindow | null): void {
    autoUpdater.autoDownload = false;
    autoUpdater.autoInstallOnAppQuit = true;

    autoUpdater.on('checking-for-update', () => {
        sendStatus(mainWindow, 'checking', 'Checking for updates…');
    });

    autoUpdater.on('update-available', (info) => {
        sendStatus(mainWindow, 'available', `Update v${info.version} available`);
        // Automatically start download
        autoUpdater.downloadUpdate();
    });

    autoUpdater.on('update-not-available', () => {
        sendStatus(mainWindow, 'current', 'You are running the latest version');
    });

    autoUpdater.on('download-progress', (progress) => {
        sendStatus(mainWindow, 'downloading', `Downloading: ${Math.round(progress.percent)}%`);
    });

    autoUpdater.on('update-downloaded', () => {
        sendStatus(mainWindow, 'ready', 'Update downloaded — will install on restart');
    });

    autoUpdater.on('error', (err) => {
        sendStatus(mainWindow, 'error', `Update error: ${err.message}`);
    });

    // Check for updates on launch (delay to allow app to settle)
    setTimeout(() => {
        autoUpdater.checkForUpdates().catch(() => { });
    }, 5000);
}

function sendStatus(win: BrowserWindow | null, status: string, message: string): void {
    win?.webContents.send('updater:status', { status, message });
}

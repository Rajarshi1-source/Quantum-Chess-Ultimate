/**
 * Quantum Chess Ultimate — Electron Main Process
 *
 * Creates the browser window, sets up native menus with keyboard shortcuts,
 * registers IPC handlers, and initializes the auto-updater.
 */

import { app, BrowserWindow, Menu, shell, dialog } from 'electron';
import * as path from 'path';
import { registerIpcHandlers } from './ipc';
import { setupAutoUpdater } from './updater';

let mainWindow: BrowserWindow | null = null;

/** URL to load — Vite dev server in dev mode, built frontend in production */
const FRONTEND_URL = process.env.VITE_DEV_URL || 'http://localhost:5173';
const IS_DEV = !app.isPackaged;

function createWindow(): void {
    mainWindow = new BrowserWindow({
        width: 1440,
        height: 900,
        minWidth: 1024,
        minHeight: 700,
        title: 'Quantum Chess Ultimate',
        backgroundColor: '#0a0b10',
        icon: path.join(__dirname, '..', 'assets', 'icon.png'),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
            sandbox: true,
        },
        show: false,
        titleBarStyle: 'hidden',
        titleBarOverlay: {
            color: '#0a0b10',
            symbolColor: '#e8eaf0',
            height: 36,
        },
    });

    // Show window when ready to avoid visual flash
    mainWindow.once('ready-to-show', () => {
        mainWindow?.show();
        mainWindow?.focus();
    });

    // Load frontend
    if (IS_DEV) {
        mainWindow.loadURL(FRONTEND_URL);
        mainWindow.webContents.openDevTools({ mode: 'detach' });
    } else {
        mainWindow.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'));
    }

    // Open external links in the system browser
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

/* ─── Native Menu ──────────────────────────────────────────── */

function buildMenu(): void {
    const template: Electron.MenuItemConstructorOptions[] = [
        {
            label: 'Game',
            submenu: [
                {
                    label: 'New Game',
                    accelerator: 'CmdOrCtrl+N',
                    click: () => mainWindow?.webContents.send('menu:new-game'),
                },
                { type: 'separator' },
                {
                    label: 'Save Game',
                    accelerator: 'CmdOrCtrl+S',
                    click: () => mainWindow?.webContents.send('menu:save-game'),
                },
                {
                    label: 'Load Game',
                    accelerator: 'CmdOrCtrl+O',
                    click: () => mainWindow?.webContents.send('menu:load-game'),
                },
                {
                    label: 'Export as PGN',
                    accelerator: 'CmdOrCtrl+Shift+E',
                    click: () => mainWindow?.webContents.send('menu:export-pgn'),
                },
                { type: 'separator' },
                { role: 'quit', accelerator: 'CmdOrCtrl+Q' },
            ],
        },
        {
            label: 'Edit',
            submenu: [
                {
                    label: 'Undo Move',
                    accelerator: 'CmdOrCtrl+Z',
                    click: () => mainWindow?.webContents.send('menu:undo'),
                },
                {
                    label: 'Redo Move',
                    accelerator: 'CmdOrCtrl+Shift+Z',
                    click: () => mainWindow?.webContents.send('menu:redo'),
                },
                { type: 'separator' },
                {
                    label: 'Flip Board',
                    accelerator: 'F',
                    click: () => mainWindow?.webContents.send('menu:flip-board'),
                },
            ],
        },
        {
            label: 'Quantum',
            submenu: [
                {
                    label: 'Toggle Quantum Overlay',
                    accelerator: 'Q',
                    click: () => mainWindow?.webContents.send('menu:toggle-quantum'),
                },
                {
                    label: 'Measure All',
                    accelerator: 'M',
                    click: () => mainWindow?.webContents.send('menu:measure-all'),
                },
                {
                    label: 'Request AI Move',
                    accelerator: 'CmdOrCtrl+Shift+A',
                    click: () => mainWindow?.webContents.send('menu:ai-move'),
                },
            ],
        },
        {
            label: 'View',
            submenu: [
                { role: 'reload' },
                { role: 'forceReload' },
                { role: 'toggleDevTools' },
                { type: 'separator' },
                { role: 'resetZoom' },
                { role: 'zoomIn' },
                { role: 'zoomOut' },
                { type: 'separator' },
                { role: 'togglefullscreen' },
            ],
        },
        {
            label: 'Help',
            submenu: [
                {
                    label: 'Quantum Chess Rules',
                    click: () => mainWindow?.webContents.send('menu:show-rules'),
                },
                {
                    label: 'GitHub Repository',
                    click: () => shell.openExternal('https://github.com/quantumchess/ultimate'),
                },
                { type: 'separator' },
                {
                    label: 'Check for Updates…',
                    click: () => mainWindow?.webContents.send('menu:check-updates'),
                },
                { type: 'separator' },
                {
                    label: `About Quantum Chess v${app.getVersion()}`,
                    click: () => {
                        dialog.showMessageBox(mainWindow!, {
                            title: 'Quantum Chess Ultimate',
                            message: `Quantum Chess Ultimate v${app.getVersion()}`,
                            detail: 'An experimental quantum chess engine exploring superposition, entanglement, and probabilistic strategy.',
                            type: 'info',
                        });
                    },
                },
            ],
        },
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

/* ─── App Lifecycle ─────────────────────────────────────────── */

app.whenReady().then(() => {
    buildMenu();
    createWindow();
    registerIpcHandlers();

    if (!IS_DEV) {
        setupAutoUpdater(mainWindow);
    }

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Security: Prevent new window creation
app.on('web-contents-created', (_event, contents) => {
    contents.on('will-navigate', (event) => {
        event.preventDefault();
    });
});

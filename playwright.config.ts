import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './e2e',
    fullyParallel: false,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: 1,
    reporter: 'html',
    timeout: 30_000,

    use: {
        baseURL: 'http://localhost:5173',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
    },

    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    ],

    webServer: [
        {
            command: process.env.CI
                ? 'cd backend && python -m uvicorn app.main:app --port 8000'
                : 'cd backend && ..\\tannie\\Scripts\\python.exe -m uvicorn app.main:app --port 8000',
            port: 8000,
            timeout: 15_000,
            reuseExistingServer: !process.env.CI,
        },
        {
            command: 'cd frontend && npm run dev',
            port: 5173,
            timeout: 15_000,
            reuseExistingServer: !process.env.CI,
        },
    ],
});

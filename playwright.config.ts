import { defineConfig, devices } from '@playwright/test';

const isCI = !!process.env.CI;

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

    // Only start local web servers outside CI. In CI, the GitHub workflow
    // is responsible for starting backend/frontend to avoid duplicate servers.
    webServer: isCI
        ? undefined
        : [
              {
                  command: 'cd backend && ..\\tannie\\Scripts\\python.exe -m uvicorn app.main:app --port 8000',
                  port: 8000,
                  timeout: 15_000,
                  reuseExistingServer: true,
              },
              {
                  command: 'cd frontend && npm run dev',
                  port: 5173,
                  timeout: 15_000,
                  reuseExistingServer: true,
              },
          ],
});

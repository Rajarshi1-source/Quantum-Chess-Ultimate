/**
 * Quantum Chess Ultimate — E2E Tests (Playwright)
 *
 * End-to-end tests for the full-stack application.
 */

import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:5173';

test.describe('Quantum Chess Ultimate', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto(BASE_URL);
    });

    test('should load the application', async ({ page }) => {
        await expect(page).toHaveTitle('Quantum Chess Ultimate');
        await expect(page.locator('h1')).toContainText('Quantum Chess');
    });

    test('should show game controls', async ({ page }) => {
        // Game controls card should be visible
        await expect(page.getByText('Game Controls')).toBeVisible();
        // Mode selector should exist
        await expect(page.locator('select')).toBeVisible();
    });

    test('should show placeholder when no game active', async ({ page }) => {
        await expect(page.getByText('No active game')).toBeVisible();
        await expect(page.getByText('Quantum Chess Ultimate').nth(0)).toBeVisible();
    });

    test('should create a new game', async ({ page }) => {
        // Click the Start button
        await page.getByRole('button', { name: /start/i }).click();

        // Wait for game to load
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Board should be visible with 8x8 squares
        const squares = page.locator('.square');
        await expect(squares).toHaveCount(64);

        // Header should show game stats
        await expect(page.getByText('Mode:')).toBeVisible();
        await expect(page.getByText('Turn:')).toBeVisible();
    });

    test('should select a square and show legal moves', async ({ page }) => {
        // Create a game first
        await page.getByRole('button', { name: /start/i }).click();
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Click on e2 pawn
        await page.locator('[data-square="e2"]').click();

        // e2 should be selected
        await expect(page.locator('[data-square="e2"]')).toHaveClass(/square-selected/);

        // Legal move indicators should appear (e3 and e4)
        await expect(page.locator('[data-square="e3"]')).toHaveClass(/square-legal/);
        await expect(page.locator('[data-square="e4"]')).toHaveClass(/square-legal/);
    });

    test('should make a move', async ({ page }) => {
        // Create a game
        await page.getByRole('button', { name: /start/i }).click();
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Select e2
        await page.locator('[data-square="e2"]').click();
        // Move to e4
        await page.locator('[data-square="e4"]').click();

        // e4 should now have the pawn (last move highlight)
        await expect(page.locator('[data-square="e4"]')).toHaveClass(/square-last-move/);

        // Turn should change
        await expect(page.getByText('● Black', { exact: true })).toBeVisible();
    });

    test('should show analysis panel after game creation', async ({ page }) => {
        await page.getByRole('button', { name: /start/i }).click();
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Analysis panel sections
        await expect(page.getByText('Status')).toBeVisible();
        await expect(page.getByText('Evaluation')).toBeVisible();
        await expect(page.getByText('Captured', { exact: true })).toBeVisible();
        await expect(page.getByText('Move History')).toBeVisible();
    });

    test('should show quantum controls', async ({ page }) => {
        await page.getByRole('button', { name: /start/i }).click();
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Quantum metrics should be visible
        await expect(page.getByText('Quantum Metrics')).toBeVisible();
        await expect(page.getByText('Superpositions', { exact: true })).toBeVisible();
        await expect(page.getByText('Entanglements')).toBeVisible();
    });

    test('should toggle quantum overlay', async ({ page }) => {
        await page.getByRole('button', { name: /start/i }).click();
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Find and click quantum toggle
        const toggle = page.getByRole('button', { name: /quantum on/i });
        await toggle.click();

        // Should now say OFF
        await expect(page.getByRole('button', { name: /quantum off/i })).toBeVisible();
    });

    test('should flip board', async ({ page }) => {
        await page.getByRole('button', { name: /start/i }).click();
        await page.waitForSelector('.chess-board', { timeout: 10000 });

        // Click flip button
        await page.getByRole('button', { name: /flip/i }).click();

        // Board should be flipped — file labels should be reversed
        // (h should be first visible file label)
        const files = page.locator('.board-files span');
        await expect(files.first()).toHaveText('h');
    });
});

test.describe('API Health', () => {
    test('backend should be healthy', async ({ request }) => {
        const resp = await request.get('http://localhost:8000/health');
        expect(resp.ok()).toBeTruthy();
        const body = await resp.json();
        expect(body.status).toBe('healthy');
    });

    test('API proxy should work through frontend', async ({ request }) => {
        const resp = await request.get(`${BASE_URL}/api/game/new`, {
            headers: { 'Content-Type': 'application/json' },
        });
        // This might be a POST-only endpoint, but proxy connectivity is what we're testing
        expect(resp.status()).toBeLessThan(500);
    });
});

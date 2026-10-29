import { defineConfig } from '@playwright/test'

const databaseUrl = 'sqlite:////tmp/ushio-e2e.db'
const apiUrl = 'http://127.0.0.1:8100'
const webUrl = 'http://127.0.0.1:4173'
const apiPython = process.env.USHIO_PYTHON ?? 'python3'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['github'], ['html', { outputFolder: 'playwright-report', open: 'never' }]] : 'list',
  outputDir: 'test-results',
  use: { baseURL: webUrl, trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  webServer: [
    { command: `rm -f /tmp/ushio-e2e.db && cd services/api && USHIO_DATABASE_URL=${databaseUrl} PYTHONPATH=. ${apiPython} -m alembic -c alembic.ini upgrade head && USHIO_DATABASE_URL=${databaseUrl} PYTHONPATH=. ${apiPython} -m uvicorn app.main:app --host 127.0.0.1 --port 8100`, cwd: '../..', url: `${apiUrl}/v1/health`, reuseExistingServer: false },
    { command: `VITE_API_BASE_URL=${apiUrl} npm run dev -- --port 4173`, cwd: '.', url: webUrl, reuseExistingServer: false },
  ],
})

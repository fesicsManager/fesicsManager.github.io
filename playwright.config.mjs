import { fileURLToPath } from 'node:url';
import { defineConfig } from '../fesics-react-web/node_modules/@playwright/test/index.mjs';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL: 'http://127.0.0.1:5191',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'python3 -m http.server 5191 --bind 127.0.0.1',
    cwd: fileURLToPath(new URL('.', import.meta.url)),
    url: 'http://127.0.0.1:5191',
    reuseExistingServer: true,
    timeout: 30_000,
  },
});

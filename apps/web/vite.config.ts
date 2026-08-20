import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // The same port `make serve` uses, so the bookmark works either way.
    port: Number(process.env.WORKBENCH_PORT ?? 5003),
    strictPort: true,
    // The API runs as a separate process in development; proxying keeps the
    // browser same-origin, so nothing depends on CORS being right.
    proxy: {
      '/api': {
        target: `http://127.0.0.1:${process.env.WORKBENCH_API_PORT ?? 8000}`,
        changeOrigin: true,
      },
    },
  },
  preview: {
    port: Number(process.env.WORKBENCH_PORT ?? 5003),
    strictPort: true,
    proxy: {
      '/api': {
        target: `http://127.0.0.1:${process.env.WORKBENCH_API_PORT ?? 8000}`,
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    css: false,
  },
})

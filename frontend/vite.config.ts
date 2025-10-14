import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isDevelopment = mode === 'development'
  
  return {
    plugins: [react()],
    server: isDevelopment ? {
      port: 3000,
      host: true,
      allowedHosts: ['localhost', '127.0.0.1', 'larospq1a.localto.net', 'tapwq0-ip-177-60-121-7.tunnelmole.net', '6drlnmx7e.localto.net'],
      proxy: {
        '^/api/v1/budgets.*': {
          target: 'http://localhost:8002',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api\/v1/, '/api/v1'),
        },
        '^/api/v1/dashboard.*': {
          target: 'http://localhost:8002',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api\/v1/, '/api/v1'),
        },
        '^/api/v1/users.*': {
          target: 'http://localhost:8001',
          changeOrigin: true,
          secure: false,
        },
        '^/api.*': {
          target: 'http://localhost:8001',
          changeOrigin: true,
          secure: false,
        },
      },
    } : undefined,
    preview: {
      port: 3000,
    },
    build: {
      outDir: 'dist',
      sourcemap: false,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            antd: ['antd'],
          },
        },
      },
    },
  }
})

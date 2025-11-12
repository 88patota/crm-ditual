import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Carrega as variáveis de ambiente baseado no modo
  const env = loadEnv(mode, process.cwd(), '')
  const isDevelopment = mode === 'development'
  
  return {
    plugins: [react()],
    // Define as variáveis de ambiente que serão expostas para o cliente
    define: {
      __VITE_API_BASE_URL__: JSON.stringify(env.VITE_API_BASE_URL),
    },
    server: isDevelopment ? {
      port: 3000,
      host: true,
      allowedHosts: ['localhost', '127.0.0.1'],
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
        onwarn(warning, warn) {
          // Suprimir warnings de referência circular que são falsos positivos
          if (warning.code === 'CIRCULAR_DEPENDENCY') {
            return;
          }
          warn(warning);
        },
        output: {
          entryFileNames: `assets/[name]-[hash].js`,
          chunkFileNames: `assets/[name]-[hash].js`,
          assetFileNames: `assets/[name]-[hash].[ext]`,
          manualChunks: {
            vendor: ['react', 'react-dom'],
            antd: ['antd'],
          },
        },
      },
    },
  }
})

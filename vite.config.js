import { defineConfig, searchForWorkspaceRoot } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

const frontendDir = path.resolve(__dirname, 'frontend')
const appDir = path.resolve(frontendDir, 'app')

export default defineConfig({
  plugins: [react()],
  root: frontendDir,
  publicDir: path.resolve(__dirname, 'static'),

  // Handle .js files with JSX syntax
  esbuild: {
    loader: 'jsx',
    include: /frontend\/.*\.js$/,
    exclude: [],
  },

  resolve: {
    alias: {
      // Libraries
      techanjs: path.resolve(__dirname, 'node_modules/techanjs/src/techan.js'),
      // App directories
      components: path.resolve(appDir, 'components'),
      security: path.resolve(appDir, 'security'),
      finance: path.resolve(appDir, 'finance'),
      site: path.resolve(appDir, 'site'),
      utils: path.resolve(appDir, 'utils'),
      configureStore: path.resolve(appDir, 'configureStore'),
      reducers: path.resolve(appDir, 'reducers'),
      sagas: path.resolve(appDir, 'sagas'),
      routes: path.resolve(appDir, 'routes'),
      config: path.resolve(appDir, 'config'),
      actions: path.resolve(appDir, 'actions'),
      api: path.resolve(appDir, 'api'),
      logging: path.resolve(appDir, 'logging'),
      constants: path.resolve(appDir, 'constants'),
      'constants.js': path.resolve(appDir, 'constants.js'),
      // Styles aliases
      '@styles': path.resolve(appDir, 'styles'),
      '@finance-styles': path.resolve(appDir, 'finance/styles'),
      // Legacy Styles
      'main.scss': path.resolve(appDir, 'styles/main.scss'),
    },
  },

  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @use "@styles/variables" as *;
        `,
        quietDeps: true,
        includePaths: [
          appDir,
          path.resolve(appDir, 'styles'),
          path.resolve(__dirname, 'node_modules'),
        ],
      },
    },
  },

  server: {
    host: true,
    port: 8888,
    fs: {
      allow: [searchForWorkspaceRoot(process.cwd())],
    },
    proxy: {
      '/api': {
        target: `http://${process.env.API_HOST || 'localhost'}:5000`,
        changeOrigin: true,
      },
      '/auth': {
        target: `http://${process.env.API_HOST || 'localhost'}:5000`,
        changeOrigin: true,
      },
    },
  },

  optimizeDeps: {
    exclude: ['techanjs'],
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
  },

  build: {
    outDir: path.resolve(__dirname, 'static'),
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'redux', 'react-redux', 'redux-saga'],
        },
      },
    },
  },
})

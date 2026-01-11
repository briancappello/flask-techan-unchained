# Migration Plan: Webpack 4 → Vite + React 18

## Overview

| Current | Target |
|---------|--------|
| Webpack 4.44.0 | Vite 5.x |
| React 16.0.0 | React 18.x |
| Babel 6.x | Vite's ESBuild |
| react-hot-loader 3.x | React Fast Refresh |
| react-loadable 5.x | React.lazy + Suspense |
| node-sass 4.x | sass (dart-sass) |
| Custom Express dev server | Vite dev server |

### Decisions Made

| Decision | Choice |
|----------|--------|
| React Version | Upgrade to React 18 |
| Dev Server | Vite's built-in proxy |
| TypeScript | No (keep JavaScript) |
| Bundle Analyzer | Remove |

---

## Phase 1: Upgrade React to v18

This should be done before the Vite migration to isolate issues.

### 1.1 Update React packages

```bash
npm install react@18 react-dom@18
npm uninstall react-loadable  # incompatible with React 18
```

### 1.2 Update entry point for React 18

Update `frontend/app/index.js`:

```js
// Before
import ReactDOM from 'react-dom'
ReactDOM.render(<App />, document.getElementById('app'))

// After
import { createRoot } from 'react-dom/client'
const root = createRoot(document.getElementById('app'))
root.render(<App store={store} history={history} />)
```

### 1.3 Replace react-loadable with React.lazy

Update `frontend/app/components/Loadable.js` to use `React.lazy` + `Suspense`.

Update all 13 page components that use the Loadable pattern:
- `frontend/app/site/pages/Home/index.js`
- `frontend/app/site/pages/Contact/index.js`
- `frontend/app/site/pages/NotFound/index.js`
- `frontend/app/security/pages/Login/index.js`
- `frontend/app/security/pages/Logout/index.js`
- `frontend/app/security/pages/SignUp/index.js`
- `frontend/app/security/pages/Profile/index.js`
- `frontend/app/security/pages/ForgotPassword/index.js`
- `frontend/app/security/pages/ResetPassword/index.js`
- `frontend/app/security/pages/PendingConfirmation/index.js`
- `frontend/app/security/pages/ResendConfirmation/index.js`
- `frontend/app/finance/pages/Chart/index.js`

### 1.4 Remove react-hot-loader

- Remove `HotReloadContainer` wrapper from entry point
- Remove `module.hot.accept` code (Vite handles this differently)
- Remove `react-hot-loader/babel` from `.babelrc`

### 1.5 Test with Webpack

Verify app still works before proceeding to Vite migration.

---

## Phase 2: Install Vite & Create Configuration

### 2.1 Install Vite dependencies

```bash
npm install -D vite @vitejs/plugin-react sass
```

### 2.2 Create `vite.config.js` in project root

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  root: 'frontend',
  publicDir: '../static',
  
  resolve: {
    alias: {
      'components': path.resolve(__dirname, 'frontend/app/components'),
      'security': path.resolve(__dirname, 'frontend/app/security'),
      'finance': path.resolve(__dirname, 'frontend/app/finance'),
      'site': path.resolve(__dirname, 'frontend/app/site'),
      'utils': path.resolve(__dirname, 'frontend/app/utils'),
      'configureStore': path.resolve(__dirname, 'frontend/app/configureStore'),
      'main.scss': path.resolve(__dirname, 'frontend/app/styles/main.scss'),
    }
  },
  
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @import "super-skeleton/scss/base/_variables.scss";
          @import "${path.resolve(__dirname, 'frontend/app/styles/_variables.scss')}";
        `,
        includePaths: [
          path.resolve(__dirname, 'frontend/app'),
          path.resolve(__dirname, 'frontend/app/styles'),
          path.resolve(__dirname, 'node_modules'),
        ]
      }
    }
  },
  
  server: {
    port: 8888,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      },
      '/auth': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  
  build: {
    outDir: '../static',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'redux', 'react-redux', 'redux-saga']
        }
      }
    }
  }
})
```

---

## Phase 3: Update HTML Entry Point

Update `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta http-equiv="x-ua-compatible" content="ie=edge">
  <title>Flask Techan Unchained</title>
</head>
<body>
  <noscript>JavaScript is required to run this app.</noscript>
  <div id="app">Loading...</div>
  <script src="/static/d3.v4.min.js"></script>
  <script type="module" src="/app/index.js"></script>
</body>
</html>
```

---

## Phase 4: Update JavaScript Entry Point

Update `frontend/app/index.js`:

```js
// Remove babel-polyfill (modern browsers don't need it)
// import 'babel-polyfill'  <-- DELETE

import 'main.scss'

import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserHistory } from 'history'  // Note: package name changed

import configureStore from 'configureStore'
import App from 'components/App'

import { login } from 'security/actions'
import { flashInfo } from 'site/actions'
import SecurityApi from 'security/api'
import { storage } from 'utils'

const initialState = {}
const history = createBrowserHistory()
const store = configureStore(initialState, history)

const root = createRoot(document.getElementById('app'))

const renderApp = () => {
  root.render(<App store={store} history={history} />)
}

// Auth check logic stays the same
const token = storage.getToken()
store.dispatch(login.request())
SecurityApi.checkAuthToken(token)
  .then(({ user }) => {
    store.dispatch(login.success({ token, user }))
  })
  .catch(() => {
    store.dispatch(login.failure())
  })
  .then(() => {
    store.dispatch(login.fulfill())
    renderApp()
    const isAuthenticated = store.getState().security.isAuthenticated
    const alreadyHasFlash = store.getState().flash.visible
    if (isAuthenticated && !alreadyHasFlash) {
      store.dispatch(flashInfo('Welcome back!'))
    }
  })
```

---

## Phase 5: Update Environment Variables

### 5.1 Create `.env` file (optional)

```env
VITE_API_URL=http://localhost:5000
```

### 5.2 Update code using `process.env`

```js
// Before (Webpack)
process.env.NODE_ENV

// After (Vite)
import.meta.env.MODE        // 'development' or 'production'
import.meta.env.DEV         // true in dev
import.meta.env.PROD        // true in prod
import.meta.env.VITE_*      // custom env vars
```

Update `frontend/app/config.js` to use Vite's env system.

---

## Phase 6: Update Loadable Component

### 6.1 Rewrite `frontend/app/components/Loadable.js`

```jsx
import React, { Suspense } from 'react'
import { useDispatch } from 'react-redux'
import { showLoading, hideLoading } from 'react-redux-loading-bar'

const LoadingFallback = () => {
  const dispatch = useDispatch()
  
  React.useEffect(() => {
    dispatch(showLoading())
    return () => dispatch(hideLoading())
  }, [dispatch])
  
  return null  // or a loading spinner
}

export const withSuspense = (LazyComponent) => {
  return function SuspenseWrapper(props) {
    return (
      <Suspense fallback={<LoadingFallback />}>
        <LazyComponent {...props} />
      </Suspense>
    )
  }
}

export default withSuspense
```

### 6.2 Update page imports (13 files)

```jsx
// Before
import Loadable from 'components/Loadable'
export default Loadable({
  loader: () => import('./Chart'),
})

// After
import { lazy } from 'react'
import withSuspense from 'components/Loadable'
export default withSuspense(lazy(() => import('./Chart')))
```

---

## Phase 7: Update package.json Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "NODE_ENV=test jest",
    "test:watch": "NODE_ENV=test jest --watchAll"
  }
}
```

---

## Phase 8: Cleanup - Remove Webpack Artifacts

### 8.1 Delete files/directories

- `frontend/internals/webpack/` (all 4 config files)
- `frontend/internals/scripts/clean.js`
- `frontend/internals/scripts/dependencies.js`
- `frontend/internals/dllConfig.js`
- `frontend/server/` (entire directory)
- `frontend/.babelrc`

### 8.2 Uninstall webpack dependencies

```bash
npm uninstall \
  webpack webpack-cli webpack-dev-middleware webpack-hot-middleware \
  html-webpack-plugin add-asset-html-webpack-plugin webpack-bundle-analyzer \
  babel-loader css-loader style-loader sass-loader file-loader url-loader \
  resolve-url-loader node-sass react-hot-loader babel-core babel-preset-env \
  babel-preset-react babel-preset-stage-0 babel-plugin-transform-async-to-generator \
  babel-plugin-transform-class-properties babel-plugin-transform-object-rest-spread \
  babel-plugin-syntax-export-extensions babel-plugin-transform-export-extensions \
  babel-plugin-transform-es2015-modules-commonjs babel-plugin-dynamic-import-node \
  express express-http-proxy minimist babel-polyfill whatwg-fetch
```

---

## Migration Checklist

| # | Task | Risk | Effort | Status |
|---|------|------|--------|--------|
| 1 | Upgrade React to v18 | Medium | 2-3 hrs | ✅ |
| 2 | Replace react-loadable with React.lazy | Low | 1-2 hrs | ✅ |
| 3 | Remove react-hot-loader | Low | 30 min | ✅ |
| 4 | Install Vite & create config | Low | 1 hr | ✅ |
| 5 | Update index.html | Low | 15 min | ✅ |
| 6 | Update entry point (index.js) | Low | 30 min | ✅ |
| 7 | Update environment variables | Low | 30 min | ✅ |
| 8 | Update SCSS configuration | Low | 30 min | ✅ |
| 9 | Update package.json scripts | Low | 15 min | ✅ |
| 10 | Remove webpack files & deps | Low | 30 min | ✅ |
| 11 | Test & fix any issues | Medium | 1-2 hrs | ✅ |

**Migration Complete!**

---

## Potential Issues to Watch For

1. **SCSS import paths** - May need adjustment for Vite's resolver
2. **D3.js external loading** - Keep the script tag, ensure it loads before app
3. **history package** - May need update (`createBrowserHistory` import path changed)
4. **redux-saga** - Should work fine, but test async flows
5. **whatwg-fetch polyfill** - Can likely be removed (modern browsers)
6. **Asset imports** - `require()` calls need to become `import`

---

## Benefits After Migration

- **Faster dev server startup** - Vite uses native ESM, no bundling needed in dev
- **Instant HMR** - React Fast Refresh is much faster than react-hot-loader
- **Smaller bundle size** - Rollup produces more optimized bundles than webpack 4
- **Modern tooling** - Better ecosystem support and maintenance
- **Simpler configuration** - Vite requires much less configuration than webpack
- **React 18 features** - Concurrent rendering, automatic batching, Suspense improvements

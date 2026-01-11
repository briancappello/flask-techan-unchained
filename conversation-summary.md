Conversation Summary: Webpack 4 to Vite Migration
What Was Done
Phase 1: React 18 Upgrade (Completed)
- Upgraded react and react-dom from v16 to v18
- Replaced react-loadable with React.lazy + Suspense in frontend/app/components/Loadable.js
- Removed react-hot-loader (Vite uses React Fast Refresh)
- Updated entry point frontend/app/index.js to use createRoot API
- Replaced node-sass with sass (dart-sass)
Phase 2: Router & Redux Ecosystem Updates (Completed)
- Replaced deprecated react-router-redux with redux-first-history@5
- Upgraded to React Router v6 (react-router-dom@6.30.3)
- Updated react-redux to v8, redux to v4, redux-saga to v1
- Replaced react-helmet with react-helmet-async
Key Files Modified for Router/Redux:
- frontend/app/configureStore.js - Uses createReduxHistoryContext from redux-first-history
- frontend/app/reducers.js - Updated to accept routerReducer as parameter
- frontend/app/components/App.js - Uses HistoryRouter from redux-first-history/rr6
- frontend/app/routes.js - Converted to React Router v6 (Routes, Route with element prop)
- frontend/app/utils/route.js - ProtectedRoute and AnonymousRoute now use hooks (useLocation, useNavigate, useSelector)
- frontend/app/site/middleware/flash.js - Uses LOCATION_CHANGE from redux-first-history
Phase 3: Vite Configuration (Completed)
- Created vite.config.js in project root with:
  - JSX handling for .js files via esbuild config
  - Path aliases matching webpack config
  - SCSS preprocessing with silenced deprecation warnings
  - API proxy configuration for /api and /auth
- Updated frontend/index.html for Vite module loading
Phase 4: ES Module Conversion (Completed)
- Converted all module.exports to ES export syntax
- Converted all require() calls to ES import statements
- Fixed export default from syntax (Babel-specific) to export { default } from
Files converted from CommonJS to ES modules:
- frontend/app/constants.js
- frontend/app/config.js
- All saga injections in page components (Login, Logout, SignUp, etc.)
- frontend/app/finance/components/ChartContainer/ChartContainer.js
- frontend/app/finance/components/Watchlists/Watchlists.js
- frontend/app/finance/components/Chart/Chart.js - Created static INDICATORS map
- frontend/app/utils/async/injectSagas.js - Converted to functional component with hooks
- frontend/app/utils/async/injectReducer.js - Converted to functional component with hooks
Phase 5: Cleanup (Completed)
- Removed frontend/internals/webpack/ directory
- Removed frontend/internals/scripts/ directory
- Removed frontend/internals/dllConfig.js
- Removed frontend/server/ directory
- Removed frontend/.babelrc
- Uninstalled ~900 webpack-related packages
- Updated package.json scripts to use Vite
Bug Fixes Applied:
1. Fixed circular dependency between routes.js and utils/route.js by hardcoding paths in route utilities
2. Fixed react-router version mismatch (had both v6 and v7 installed) - now using v6.30.3
Current State
Vite dev server starts successfully (npm run dev), but there's still a runtime error:
useRoutes() may be used only in the context of a <Router> component
What Needs Investigation
The useRoutes error persists even after fixing the react-router version mismatch. Possible causes to investigate:
1. Order of Provider nesting in frontend/app/components/App.js - The HistoryRouter may need to be higher in the tree
2. Lazy-loaded components using router hooks before Router context is available
3. HOC composition order - injectSagas and injectReducer HOCs might be causing issues
Key Configuration Files
- vite.config.js - Vite configuration
- frontend/app/configureStore.js - Redux store with redux-first-history
- frontend/app/components/App.js - Root component with Provider/Router setup
- frontend/app/routes.js - Route definitions
- package.json - Current dependencies
Commands
- npm run dev - Start Vite dev server
- npm run build - Build for production
Next Steps
1. Debug the useRoutes() context error - likely need to check if something is rendering outside the Router context
2. Test the application functionality once router error is resolved
3. Verify production build works with npm run build

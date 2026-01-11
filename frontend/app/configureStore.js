import { applyMiddleware, compose, createStore } from 'redux'
import { createReduxHistoryContext } from 'redux-first-history'
import { createBrowserHistory } from 'history'
import { loadingBarMiddleware } from 'react-redux-loading-bar'
import createSagaMiddleware from 'redux-saga'

import createReducer from 'reducers'
import getSagas from 'sagas'
import { flashClearMiddleware } from 'site/middleware/flash'

const isDev = import.meta.env.MODE !== 'production'
const hasWindowObject = typeof window === 'object'

const sagaMiddleware = createSagaMiddleware()

const { createReduxHistory, routerMiddleware, routerReducer } =
  createReduxHistoryContext({
    history: createBrowserHistory(),
  })

export { routerReducer }

export default function configureStore(initialState) {
  const middlewares = [
    sagaMiddleware,
    routerMiddleware,
    loadingBarMiddleware({ promiseTypeSuffixes: ['REQUEST', 'FULFILL'] }),
    flashClearMiddleware,
  ]

  const enhancers = [applyMiddleware(...middlewares)]

  const composeEnhancers =
    isDev && hasWindowObject && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
      ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
      : compose

  const store = createStore(
    createReducer(routerReducer),
    initialState,
    composeEnhancers(...enhancers),
  )

  // extensions
  store.runSaga = sagaMiddleware.run
  store.injectedReducers = {}
  store.injectedSagas = {}
  store.routerReducer = routerReducer

  let runningSagas = sagaMiddleware.run(function* () {
    yield getSagas()
  })

  if (import.meta.hot) {
    import.meta.hot.accept('./reducers', async () => {
      const { default: nextCreateReducer } = await import('./reducers')
      store.replaceReducer(nextCreateReducer(routerReducer, store.injectedReducers))
    })

    import.meta.hot.accept('./sagas', async () => {
      const { default: nextGetSagas } = await import('./sagas')
      runningSagas.cancel()
      runningSagas.done.then(() => {
        runningSagas = sagaMiddleware.run(function* () {
          yield nextGetSagas()
        })
      })
    })
  }

  const history = createReduxHistory(store)

  return { store, history }
}

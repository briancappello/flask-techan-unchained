// this must come before everything else otherwise style cascading doesn't work as expected
import 'main.scss'

import React from 'react'
import { createRoot } from 'react-dom/client'

import configureStore from 'configureStore'
import App from 'components/App'

import { login } from 'security/actions'
import { flashInfo } from 'site/actions'
import SecurityApi from 'security/api'
import { storage } from 'utils'

const APP_MOUNT_POINT = document.getElementById('app')

const initialState = {}
const { store, history } = configureStore(initialState)

const root = createRoot(APP_MOUNT_POINT)

const renderApp = () => {
  root.render(<App store={store} history={history} />)
}

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

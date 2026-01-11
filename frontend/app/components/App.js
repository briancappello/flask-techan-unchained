import React from 'react'
import { Provider } from 'react-redux'
import { HistoryRouter as Router } from 'redux-first-history/rr6'
import { HelmetProvider, Helmet } from 'react-helmet-async'

import { ProgressBar } from 'components'
import { SITE_NAME } from 'config'
import Routes from 'routes'

import 'main.scss'

const AppLayout = () => (
  <div className="fixed-nav-top">
    <Helmet titleTemplate={`%s - ${SITE_NAME}`} defaultTitle={SITE_NAME} />
    <ProgressBar />
    <Routes />
  </div>
)

export default (props) => (
  <Provider store={props.store}>
    <HelmetProvider>
      <Router history={props.history}>
        <AppLayout />
      </Router>
    </HelmetProvider>
  </Provider>
)

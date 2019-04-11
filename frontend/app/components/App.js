import React from 'react'
import { Provider } from 'react-redux'
import { ConnectedRouter } from 'react-router-redux'
import Helmet from 'react-helmet'

import { ProgressBar } from 'components'
import { SITE_NAME } from 'config'
import Routes from 'routes'

import 'main.scss'

const AppLayout = () => (
  <div className="fixed-nav-top">
    <Helmet titleTemplate={`%s - ${SITE_NAME}`}
            defaultTitle={SITE_NAME}
    />
    <ProgressBar />
    <Routes />
  </div>
)

export default (props) => (
  <Provider store={props.store}>
    <ConnectedRouter history={props.history}>
      <AppLayout />
    </ConnectedRouter>
  </Provider>
)

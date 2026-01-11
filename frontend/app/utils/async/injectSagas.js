import React, { useEffect, useContext, useRef } from 'react'
import hoistNonReactStatics from 'hoist-non-react-statics'
import get from 'lodash/get'
import { ReactReduxContext } from 'react-redux'
import { all } from 'redux-saga/effects'

import getInjectors from './sagaInjectors'

/**
 * Dynamically injects a saga, passes component's props as saga arguments
 *
 * @param {Object} props
 * @param {string} props.key A key of the saga
 * @param {function} props.sagas A fn returning sagas to be injected
 * @param {string} [props.mode] By default, constants.DAEMON
 *   - constants.RESTART_ON_REMOUNT - the saga will be started on component mount and cancelled with `task.cancel()` on component un-mount for improved performance.
 *   - constants.DAEMON — starts the saga on component mount and never cancels it or starts again.
 *   - constants.ONCE_TILL_UNMOUNT — behaves like 'RESTART_ON_REMOUNT' but never runs it again.
 *
 */
export default (moduleOrProps) => (WrappedComponent) => {
  let props = moduleOrProps

  // Handle ES module format (from dynamic import or require)
  if (get(props, '__esModule', false) || get(props, 'default')) {
    props = {
      key: props.KEY,
      sagas: props.default,
      mode: get(props, 'MODE', null),
    }
  }

  const InjectSaga = (componentProps) => {
    const { store } = useContext(ReactReduxContext)
    const injectedRef = useRef(false)

    // create a root saga to inject
    const saga = function* () {
      const effects = props.sagas()
      yield all(Array.isArray(effects) ? effects : [effects])
    }

    // Inject saga synchronously on first render (before children render)
    // This ensures that if the child dispatches an action in useEffect,
    // the saga is already listening.
    if (!injectedRef.current) {
      const injectors = getInjectors(store)
      injectors.injectSaga(props.key, { saga, mode: props.mode }, componentProps)
      injectedRef.current = true
    }

    useEffect(() => {
      return () => {
        const injectors = getInjectors(store)
        injectors.ejectSaga(props.key)
      }
    }, [store])

    return <WrappedComponent {...componentProps} />
  }

  InjectSaga.displayName = `withSaga(${WrappedComponent.displayName || WrappedComponent.name || 'Component'})`
  InjectSaga.WrappedComponent = WrappedComponent

  return hoistNonReactStatics(InjectSaga, WrappedComponent)
}

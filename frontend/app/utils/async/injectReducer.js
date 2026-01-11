import React, { useEffect, useContext, useRef } from 'react'
import hoistNonReactStatics from 'hoist-non-react-statics'
import get from 'lodash/get'
import { ReactReduxContext } from 'react-redux'

import getInjectors from './reducerInjectors'


/**
 * Dynamically injects a reducer
 *
 * @param {string} key A key of the reducer
 * @param {function} reducer A reducer that will be injected
 *
 */
export default (moduleOrProps) => (WrappedComponent) => {
  let props = moduleOrProps
  
  // Handle ES module format (from dynamic import or require)
  if (get(props, '__esModule', false) || get(props, 'default')) {
    props = {
      key: props.KEY,
      reducer: props.default,
    }
  }

  const ReducerInjector = (componentProps) => {
    const { store } = useContext(ReactReduxContext)
    const injectedRef = useRef(false)
    
    // Inject reducer synchronously on first render (before children render)
    if (!injectedRef.current) {
      const injectors = getInjectors(store)
      injectors.injectReducer(props.key, props.reducer)
      injectedRef.current = true
    }

    return <WrappedComponent {...componentProps} />
  }
  
  ReducerInjector.displayName = `withReducer(${(WrappedComponent.displayName || WrappedComponent.name || 'Component')})`
  ReducerInjector.WrappedComponent = WrappedComponent

  return hoistNonReactStatics(ReducerInjector, WrappedComponent)
}

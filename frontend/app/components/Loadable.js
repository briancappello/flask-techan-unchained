import React, { Suspense, useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { showLoading, hideLoading } from 'react-redux-loading-bar'

/**
 * Loading fallback component that integrates with react-redux-loading-bar
 *
 * The ProgressBar component is already rendered by components/App.js,
 * and it listens for the actions we're dispatching from this component's
 * lifecycle events
 */
const LoadingFallback = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(showLoading())
    return () => dispatch(hideLoading())
  }, [dispatch])

  return null
}

/**
 * HOC to wrap a lazy-loaded component with Suspense and loading bar integration
 */
export const withSuspense = (LazyComponent) => {
  return function SuspenseWrapper(props) {
    return (
      <Suspense fallback={<LoadingFallback />}>
        <LazyComponent {...props} />
      </Suspense>
    )
  }
}

/**
 * Helper function that mimics the old Loadable API for easier migration
 * Supports both:
 *   - createLoadable(() => import('./MyComponent'))
 *   - createLoadable({ loader: () => import('./MyComponent') })
 */
export const createLoadable = (importFnOrConfig) => {
  const importFn =
    typeof importFnOrConfig === 'function' ? importFnOrConfig : importFnOrConfig.loader
  const LazyComponent = React.lazy(importFn)
  return withSuspense(LazyComponent)
}

export default createLoadable

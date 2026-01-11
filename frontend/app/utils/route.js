import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Navigate, useLocation, useNavigate, useSearchParams } from 'react-router-dom'

import { flashInfo } from 'site/actions'


/**
 * ProtectedRoute - Only allows authenticated users
 * Redirects to login page if not authenticated
 */
export const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useSelector((state) => state.security.isAuthenticated)
  const location = useLocation()

  if (!isAuthenticated) {
    return (
      <Navigate
        to={{
          pathname: '/login',
          search: `?next=${encodeURIComponent(location.pathname + location.search)}`,
        }}
        replace
      />
    )
  }

  return children
}


/**
 * AnonymousRoute - Only allows non-authenticated users
 * Redirects to home page if already authenticated
 */
export const AnonymousRoute = ({ children }) => {
  const isAuthenticated = useSelector((state) => state.security.isAuthenticated)
  const isFlashVisible = useSelector((state) => state.flash.visible)
  const dispatch = useDispatch()
  const location = useLocation()

  useEffect(() => {
    if (isAuthenticated && !isFlashVisible && location.pathname === '/login') {
      dispatch(flashInfo('You are already logged in.'))
    }
  }, [isAuthenticated, isFlashVisible, dispatch, location.pathname])

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  // Still render children even if authenticated to avoid flash of content
  // The useEffect will handle the redirect
  return children
}

import React from 'react'
import { Routes, Route } from 'react-router-dom'
import startCase from 'lodash/startCase'
import { compile } from 'path-to-regexp'

import { Chart } from 'finance/pages'

import {
  ForgotPassword,
  Login,
  Logout,
  PendingConfirmation,
  Profile,
  SignUp,
  ResendConfirmation,
  ResetPassword,
} from 'security/pages'

import { Contact, Home, NotFound } from 'site/pages'

import { AnonymousRoute, ProtectedRoute } from 'utils/route'

/**
 * ROUTES: The canonical store of frontend routes. Routes throughout the system
 * should be referenced using these constants
 *
 * Both keys and values are component class names
 */
export const ROUTES = {
  Chart: 'Chart',
  Contact: 'Contact',
  ForgotPassword: 'ForgotPassword',
  Home: 'Home',
  Login: 'Login',
  Logout: 'Logout',
  PendingConfirmation: 'PendingConfirmation',
  Profile: 'Profile',
  ResendConfirmation: 'ResendConfirmation',
  ResetPassword: 'ResetPassword',
  SignUp: 'SignUp',
}

/**
 * route details
 *
 * list of objects with keys:
 *  - key: component class name
 *  - path: the path for the component (in react router notation)
 *  - component: The component to use
 *  - routeType: optional, 'anonymous', 'protected', or null (default: null for public)
 *  - label: optional, label to use for links (default: startCase(key))
 */
const routes = [
  {
    key: ROUTES.Chart,
    path: '/finance/chart/:ticker',
    routeType: 'protected',
    component: Chart,
  },
  {
    key: ROUTES.Contact,
    path: '/contact',
    component: Contact,
  },
  {
    key: ROUTES.ForgotPassword,
    path: '/login/forgot-password',
    component: ForgotPassword,
    routeType: 'anonymous',
    label: 'Forgot password?',
  },
  {
    key: ROUTES.Home,
    path: '/',
    component: Home,
  },
  {
    key: ROUTES.Login,
    path: '/login',
    component: Login,
    routeType: 'anonymous',
    label: 'Login',
  },
  {
    key: ROUTES.Logout,
    path: '/logout',
    component: Logout,
    label: 'Logout',
  },
  {
    key: ROUTES.PendingConfirmation,
    path: '/sign-up/pending-confirm-email',
    component: PendingConfirmation,
    routeType: 'anonymous',
    label: 'Pending Confirm Email',
  },
  {
    key: ROUTES.Profile,
    path: '/profile',
    component: Profile,
    routeType: 'protected',
    label: 'Profile',
  },
  {
    key: ROUTES.ResendConfirmation,
    path: '/sign-up/resend-confirmation-email',
    component: ResendConfirmation,
    routeType: 'anonymous',
    label: 'Resend Confirmation Email',
  },
  {
    key: ROUTES.ResetPassword,
    path: '/login/reset-password/:token',
    component: ResetPassword,
    routeType: 'anonymous',
    label: 'Reset Password',
  },
  {
    key: ROUTES.SignUp,
    path: '/sign-up',
    component: SignUp,
    routeType: 'anonymous',
    label: 'Sign Up',
  },
]

/**
 * ROUTE_MAP: A public lookup for route details by key
 */
export const ROUTE_MAP = {}
routes.forEach((route) => {
  let { component, key, label, path, routeType } = route

  if (!component) {
    throw new Error(`component was not specified for the ${key} route!`)
  }
  if (!path) {
    throw new Error(`path was not specified for the ${key} route!`)
  }

  ROUTE_MAP[key] = {
    path,
    toPath: compile(path),
    component,
    routeType: routeType || null,
    label: label || startCase(key),
  }
})

/**
 * Wrap component based on route type
 */
const wrapComponent = (Component, routeType) => {
  if (routeType === 'protected') {
    return (
      <ProtectedRoute>
        <Component />
      </ProtectedRoute>
    )
  }
  if (routeType === 'anonymous') {
    return (
      <AnonymousRoute>
        <Component />
      </AnonymousRoute>
    )
  }
  return <Component />
}

export default () => (
  <Routes>
    {routes.map((route) => {
      const { component: Component, path, routeType } = ROUTE_MAP[route.key]
      return (
        <Route key={path} path={path} element={wrapComponent(Component, routeType)} />
      )
    })}
    <Route path="*" element={<NotFound />} />
  </Routes>
)

import React, { useMemo } from 'react'
import PropTypes from 'prop-types'
import { NavLink } from 'react-router-dom'
import { stringify } from 'query-string'

import { ROUTE_MAP } from 'routes'


const LoadableNavLink = ({ children, to, params = {}, queryParams = {}, className, ...props }) => {
  const route = useMemo(() => ROUTE_MAP[to], [to])

  const toPath = useMemo(() => ({
    pathname: route ? route.toPath(params) : to,
    search: Object.keys(queryParams).length ? `?${stringify(queryParams)}` : '',
  }), [route, to, params, queryParams])

  return (
    <NavLink
      {...props}
      className={({ isActive }) =>
        [className, isActive ? 'active' : ''].filter(Boolean).join(' ')
      }
      to={toPath}
    >
      {children || (route && route.label)}
    </NavLink>
  )
}

LoadableNavLink.propTypes = {
  children: PropTypes.node,
  to: PropTypes.string,
  params: PropTypes.object,
  queryParams: PropTypes.object,
  className: PropTypes.string,
}

export default LoadableNavLink

import React from 'react'
import PropTypes from 'prop-types'
import { NavLink } from 'react-router-dom'
import isFunction from 'lodash/isFunction'
import { stringify } from 'query-string'

import { ROUTE_MAP } from 'routes'


export default class LoadableNavLink extends React.Component {

  static propTypes = {
    children: PropTypes.node,
    to: PropTypes.string,
    params: PropTypes.object,
    queryParams: PropTypes.object,
  }

  static defaultProps = {
    queryParams: {},
  }

  constructor(props) {
    super(props)
    this.route = ROUTE_MAP[props.to]
  }

  componentWillReceiveProps(nextProps) {
    this.route = ROUTE_MAP[nextProps.to]
  }

  maybePreloadComponent = () => {
    if (!this.route) {
      return
    }

    const { component } = this.route
    if (isFunction(component.preload)) {
      component.preload()
    }
  }

  render() {
    const { children, to, params, queryParams, ...props } = this.props
    return (
      <NavLink {...props}
               activeClassName="active"
               onMouseOver={this.maybePreloadComponent}
               to={{
                 pathname: this.route ? this.route.toPath(params) : to,
                 search: Object.keys(queryParams).length ? `?${stringify(queryParams)}` : '',
               }}
      >
        {children || this.route.label}
      </NavLink>
    )
  }
}

import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import { useLocation } from 'react-router-dom'
import classnames from 'classnames'

import { ROUTES } from 'routes'
import NavLink from './NavLink'

import './navbar.scss'

const NavBar = () => {
  const [menuOpen, setMenuOpen] = useState(false)
  const isAuthenticated = useSelector((state) => state.security.isAuthenticated)
  const location = useLocation()

  // Close menu on location change
  useEffect(() => {
    setMenuOpen(false)
  }, [location])

  const toggleResponsiveMenu = () => {
    setMenuOpen(!menuOpen)
  }

  const renderAuthenticatedMenu = () => (
    <div>
      <NavLink to={ROUTES.Profile} />
      <NavLink to={ROUTES.Logout} />
    </div>
  )

  const renderUnauthenticatedMenu = () => (
    <div>
      <NavLink to={ROUTES.SignUp} />
      <NavLink to={ROUTES.Login} />
    </div>
  )

  return (
    <nav className={classnames({ 'menu-open': menuOpen })}>
      <div className="container navbar-top">
        <NavLink end to={ROUTES.Home} className="brand">
          Flask Techan Unchained
        </NavLink>
        <a
          href="#"
          className="burger"
          onClick={(e) => {
            e.preventDefault()
            toggleResponsiveMenu()
          }}
        >
          Menu&nbsp;&nbsp;&#9776;
        </a>
        <div className="menu left">
          <NavLink to={ROUTES.Contact} />
        </div>
        <div className="menu right">
          {isAuthenticated ? renderAuthenticatedMenu() : renderUnauthenticatedMenu()}
        </div>
      </div>
    </nav>
  )
}

export default NavBar

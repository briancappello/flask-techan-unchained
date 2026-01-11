import React from 'react'
import { useLocation } from 'react-router-dom'

import Flash from 'components/Flash'
import { NavBar, ScrollIntoView } from 'components/Nav'
import { COPYRIGHT } from 'config'

const PageContent = ({ children, className = '' }) => {
  const location = useLocation()
  const hash = location.hash

  return (
    <main>
      <header>
        <NavBar />
      </header>
      <div className="container">
        <Flash />
        <div className={`${className} content`}>
          <ScrollIntoView id={(hash && hash.slice(1)) || null}>
            {children}
          </ScrollIntoView>
        </div>
      </div>
      <footer className="center">
        Copyright {new Date().getFullYear()} {COPYRIGHT}
      </footer>
    </main>
  )
}

export default PageContent

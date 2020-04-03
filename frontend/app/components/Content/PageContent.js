import React from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router'

import Flash from 'components/Flash'
import { NavBar, ScrollIntoView } from 'components/Nav'
import { COPYRIGHT } from 'config'


class PageContent extends React.Component {

  static defaultProps = {
    className: '',
  }

  render() {
    const { children, className, location: { hash } } = this.props
    return (
      <main>
        <header>
          <NavBar />
        </header>
        <div className="container">
          <Flash />
          <div className={`${className} content`}>
            <ScrollIntoView id={hash && hash.slice(1) || null}>
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
}

export default withRouter(PageContent)

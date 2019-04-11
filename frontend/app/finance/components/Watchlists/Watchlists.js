import React from 'react'
import { bindActionCreators, compose } from 'redux'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'

import { bindRoutineCreators } from 'actions'
import { NavLink } from "components/Nav";
import { ROUTES } from 'routes'
import injectSagas from 'utils/async/injectSagas'

import { loadWatchlists, loadWatchlist } from 'finance/actions'
import { selectWatchlists, selectWatchlistComponents } from 'finance/selectors'

import './watchlists.scss'
import classnames from "classnames"


class Watchlists extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      sidebarListHeight: this._getSidebarListHeight(),
    }
  }

  componentWillMount() {
    const { loadWatchlists, loadWatchlist } = this.props
    loadWatchlists.maybeTrigger()
    loadWatchlist.maybeTrigger({ key: '^DJI' })
    loadWatchlist.maybeTrigger({ key: '^DJT' })
    loadWatchlist.maybeTrigger({ key: '^NDX' })
  }

  componentDidMount() {
    window.addEventListener('resize', this.handleResize)
  }

  handleResize = () => {
    this.setState({
      sidebarListHeight: this._getSidebarListHeight(),
    })
  }

  _getSidebarListHeight() {
    const height = Math.max(document.documentElement.clientHeight, window.innerHeight)
    const formHeight = 48
    const paddingTop = 10

    return height - (formHeight + paddingTop)
  }

  render() {
    const { watchlistComponents, queryParams } = this.props
    const { sidebarListHeight } = this.state
    return (
      <div className="watchlists" style={{ height: sidebarListHeight }}>
        {Object.keys(watchlistComponents).map((watchlistKey) => {
          const list = watchlistComponents[watchlistKey]
          return (
            <div key={watchlistKey}>
              <div className="watchlist-key">
                {watchlistKey}
              </div>
              <ul>
                {list.map((quote) => {
                  const change = quote.close - quote.prev_close
                  const pctChange = 100 * change / quote.prev_close
                  return (
                    <li key={quote.ticker}>
                    <span className="ticker">
                      <NavLink to={ROUTES.Chart} params={{ ticker: quote.ticker }} queryParams={queryParams}>
                        {quote.ticker}
                      </NavLink>
                    </span>
                      <span className="quote">
                        <span className="price">
                          {quote.close.toFixed(2)}
                        </span>
                        <br/>
                        <span className={`change ${classnames({
                          up: change > 0,
                          down: change < 0,
                        })}`}>
                          {change > 0 && '+'}{change.toFixed(2)}{' '}
                          ({change > 0 && '+'}{pctChange.toFixed(2)}%)
                        </span>
                      </span>
                    </li>
                  )
                })}
              </ul>
            </div>
          )
        })}
      </div>
    )
  }
}

const withWatchlistSagas = injectSagas(require('finance/sagas/loadWatchlist'))
const withWatchlistsSagas = injectSagas(require('finance/sagas/loadWatchlists'))

const withConnect = connect(
  (state) => ({
    watchlistComponents: selectWatchlistComponents(state),
    watchlists: selectWatchlists(state),
  }),
  (dispatch) => ({
    ...bindActionCreators({ push }, dispatch),
    ...bindRoutineCreators({ loadWatchlist, loadWatchlists }, dispatch),
  })
)

export default compose(
  withWatchlistSagas,
  withWatchlistsSagas,
  withConnect,
)(Watchlists)

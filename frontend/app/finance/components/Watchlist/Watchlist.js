import React from 'react'
import PropTypes from 'prop-types'

import classnames from "classnames"

import { NavLink } from 'components/Nav'
import { ROUTES } from 'routes'

import './watchlist.scss'


class Watchlist extends React.Component {

  static propTypes = {
    watchlistKey: PropTypes.string.isRequired,
    quotes: PropTypes.arrayOf(PropTypes.shape({
      ticker: PropTypes.string.isRequired,
      open: PropTypes.number.isRequired,
      high: PropTypes.number.isRequired,
      low: PropTypes.number.isRequired,
      close: PropTypes.number.isRequired,
      prev_close: PropTypes.number.isRequired,
    })).isRequired
  }

  render() {
    const { watchlistKey, quotes, queryParams } = this.props
    return (
      <div className="watchlist">
        <div className="watchlist-key">
          {watchlistKey}
        </div>
        <ul>
          {quotes.map((quote) => {
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
  }
}

export default Watchlist

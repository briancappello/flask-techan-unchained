// Flask Techan Unchained
//
// Copyright (C) 2020  Brian Cappello
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

import React from 'react'
import PropTypes from 'prop-types'

import classnames from "classnames"

import { NavLink } from 'components/Nav'
import { ROUTES } from 'routes'

import './watchlist.scss'


class Watchlist extends React.Component {

  static propTypes = {
    watchlist: PropTypes.string.isRequired,
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
    const { watchlist, quotes, queryParams } = this.props
    return (
      <div className="watchlist">
        <div className="watchlist-key">
          {watchlist}
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

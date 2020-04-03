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

import { v1 } from 'api'
import { get, post } from 'utils/request'


function finance(uri, queryParams) {
  return v1(`/finance${uri}`, queryParams)
}

export default class FinanceApi {
  static loadTickerHistory(ticker, frequency) {
    return get(finance(`/history/${ticker}`, { frequency }))
  }

  static loadWatchlist(key) {
    return get(finance(`/watchlists/${key}`))
  }

  static loadWatchlists() {
    return get(finance('/watchlists'))
  }
}

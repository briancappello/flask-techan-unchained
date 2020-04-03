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

import { createRoutine } from 'actions'

export const SHOW_WATCHLIST = 'SHOW_WATCHLIST'
export const HIDE_WATCHLIST = 'HIDE_WATCHLIST'

export const showWatchlist = (key) => ({
  type: SHOW_WATCHLIST,
  payload: { key },
})
export const hideWatchlist = (key) => ({
  type: HIDE_WATCHLIST,
  payload: { key },
})

export const loadWatchlist = createRoutine('finance/LOAD_WATCHLIST')
export const loadWatchlists = createRoutine('finance/LOAD_WATCHLISTS')

export const loadTickerHistory = createRoutine('finance/LOAD_TICKER_HISTORY')

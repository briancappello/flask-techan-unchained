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

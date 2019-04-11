export const selectWatchlistsState = (state) => state.finance.watchlists

// all watchlists

export const areWatchlistsLoaded = (state) => {
  return selectWatchlistsState(state).isLoaded
}

export const areWatchlistsLoading = (state) => {
  return selectWatchlistsState(state).isLoading
}

export const selectWatchlists = (state) => {
  const watchlists = selectWatchlistsState(state).watchlists
  return Object.keys(watchlists).map(key => watchlists[key])
}

// individual watchlists

export const isWatchlistLoaded = (state, key) => {
  const watchlistState = selectWatchlistsState(state).watchlists[key]
  return watchlistState && watchlistState.isLoaded
}

export const isWatchlistLoading = (state, key) => {
  const watchlistState = selectWatchlistsState(state).watchlists[key]
  return watchlistState && watchlistState.isLoading
}

// chart watchlists
// FIXME: make selected watchlists on a per-chart basis
export const selectWatchlistComponents = (state) => {
  const watchlistsState = selectWatchlistsState(state)
  return Object.keys(watchlistsState.watchlists).reduce((watchlists, key) => {
    let watchlistState = watchlistsState.watchlists[key]
    if (watchlistState.isLoaded) {
      watchlists[key] = watchlistState.components
    }
    return watchlists
  }, {})
}

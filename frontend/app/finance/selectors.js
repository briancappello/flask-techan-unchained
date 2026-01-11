import { createSelector } from 'reselect'

export const selectWatchlistsState = (state) => state.finance.watchlists

// all watchlists

export const areWatchlistsLoaded = (state) => {
  return selectWatchlistsState(state).isLoaded
}

export const areWatchlistsLoading = (state) => {
  return selectWatchlistsState(state).isLoading
}

export const selectWatchlistsMap = (state) => selectWatchlistsState(state).watchlists

export const selectWatchlists = createSelector(
  [selectWatchlistsMap],
  (watchlists) => Object.keys(watchlists).map(key => watchlists[key])
)

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
export const selectWatchlistComponents = createSelector(
  [selectWatchlistsMap],
  (watchlists) => {
    const result = {}
    let hasChanged = false
    Object.keys(watchlists).forEach(key => {
      const watchlistState = watchlists[key]
      if (watchlistState.isLoaded) {
        result[key] = {
          label: watchlistState.label,
          components: watchlistState.components,
        }
      }
    })
    return result
  }
)

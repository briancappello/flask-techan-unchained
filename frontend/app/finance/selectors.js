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
      watchlists[key] = {
        label: watchlistState.label,
        components: watchlistState.components,
      }
    }
    return watchlists
  }, {})
}

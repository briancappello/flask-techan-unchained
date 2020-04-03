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

import { loadWatchlist, loadWatchlists } from 'finance/actions'


export const initialState = {
  watchlists: {},
  isLoaded: false,
  isLoading: false,
}

const initialWatchlistState = {
  key: null,
  label: null,
  components: [],
  isLoaded: false,
  isLoading: false,
}

export default function (state = initialState, action) {
  const { type, payload } = action
  const { key, watchlist } = payload || {}

  if (!payload) {
    return state
  }

  switch (type) {
    // -------------------------------------------------------------------------
    // loadWatchlists
    // -------------------------------------------------------------------------
    case loadWatchlists.REQUEST:
      return { ...state,
        isLoading: true,
      }

    case loadWatchlists.SUCCESS:
      return { ...state,
        watchlists: payload.watchlists.reduce((watchlists, watchlist) => {
          watchlists[watchlist.key] = Object.assign({}, initialWatchlistState, watchlist)
          return watchlists
        }, {}),
        isLoaded: true,
      }

    case loadWatchlists.FAILURE:
      return { ...state,
        isLoaded: false,
      }

    case loadWatchlists.FULFILL:
      return { ...state,
        isLoading: false,
      }

    // -------------------------------------------------------------------------
    // loadWatchlist
    // -------------------------------------------------------------------------
    case loadWatchlist.REQUEST:
      return { ...state,
        watchlists: { ...state.watchlists,
          [key]: {
            ...Object.assign({}, initialWatchlistState, state.watchlists[key]),
            isLoading: true,
          },
        },
      }

    case loadWatchlist.SUCCESS:
      return { ...state,
        watchlists: { ...state.watchlists,
          [key]: { ...state.watchlists[key],
            isLoaded: true,
            ...watchlist,
          }
        }
      }

    case loadWatchlist.FAILURE:
      return { ...state,
        watchlists: { ...state.watchlists,
          [key]: { ...state.watchlists[key],
            isLoaded: false,
          }
        }
      }

    case loadWatchlist.FULFILL:
      return { ...state,
        watchlists: { ...state.watchlists,
          [key]: { ...state.watchlists[key],
            isLoading: false,
          }
        }
      }

    default:
      return state
  }
}

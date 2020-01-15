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

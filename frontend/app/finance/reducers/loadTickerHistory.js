import { loadTickerHistory } from 'finance/actions'


export const KEY = 'loadTickerHistory'

const tickerInitialState = {
  isLoading: false,
  lastUpdated: null,
  history: {},
}

const initialState = {
  tickers: {},
}

export default function (state = initialState, action) {
  const { type, payload } = action

  const { ticker, frequency, history } = payload || {}
  let tickerState

  switch (type) {
    case loadTickerHistory.REQUEST:
      tickerState = Object.assign({}, tickerInitialState, state.tickers[ticker])
      return { ...state,
        tickers: { ...state.tickers,
          [ticker]: { ...tickerState,
            isLoading: frequency,
          },
        },
      }

    case loadTickerHistory.SUCCESS:
      tickerState = Object.assign({}, state.tickers[ticker])
      return { ...state,
        tickers: { ...state.tickers,
          [ticker]: { ...tickerState,
            lastUpdated: new Date(),
            history: { ...tickerState.history,
              [frequency]: history,
            },
          },
        },
      }

    case loadTickerHistory.FULFILL:
      tickerState = Object.assign({}, state.tickers[ticker])
      return { ...state,
        tickers: { ...state.tickers,
          [ticker]: { ...tickerState,
            isLoading: false,
          },
        },
      }

    default:
      return state
  }
}

export const selectTickers = (state) => state[KEY].tickers
export const hasTickerHistory = (state, ticker, frequency) => {
  const tickers = selectTickers(state)
  return !!(
    tickers[ticker]
    && tickers[ticker].history
    && tickers[ticker].history[frequency]
  )
}
export const isTickerHistoryLoading = (state, ticker, frequency) => {
  const tickers = selectTickers(state)
  return tickers[ticker] && (tickers[ticker].isLoading == frequency)
}
export const selectHistoryByTicker = (state, ticker, frequency) => {
  const tickers = selectTickers(state)
  return tickers[ticker] && tickers[ticker].history[frequency]
}

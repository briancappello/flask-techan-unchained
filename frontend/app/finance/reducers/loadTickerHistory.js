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

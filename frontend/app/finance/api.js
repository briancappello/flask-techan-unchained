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

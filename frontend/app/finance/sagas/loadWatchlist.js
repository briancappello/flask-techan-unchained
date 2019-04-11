import { call, put, select, takeEvery } from 'redux-saga/effects'

import { createRoutineSaga } from 'sagas'

import { loadWatchlist } from 'finance/actions'
import FinanceApi from 'finance/api'
import { isWatchlistLoaded, isWatchlistLoading } from 'finance/selectors'

export const KEY = 'loadWatchlist'


export function *maybeLoadWatchlistSaga({ payload: { key } }) {
  const isLoaded = yield select(isWatchlistLoaded, key)
  const isLoading = yield select(isWatchlistLoading, key)
  if (!(isLoaded || isLoading)) {
    yield put(loadWatchlist.trigger({ key }))
  }
}

export const loadWatchlistSaga = createRoutineSaga(
  loadWatchlist,
  function *({ key }) {
    const watchlist = yield call(FinanceApi.loadWatchlist, key)
    yield put(loadWatchlist.success({ key, watchlist }))
  }
)

export default () => [
  takeEvery(loadWatchlist.MAYBE_TRIGGER, maybeLoadWatchlistSaga),
  takeEvery(loadWatchlist.TRIGGER, loadWatchlistSaga),
]

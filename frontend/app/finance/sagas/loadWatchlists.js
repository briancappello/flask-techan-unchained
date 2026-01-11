import { call, put, select, takeEvery } from 'redux-saga/effects'

import { loadWatchlists } from 'finance/actions'
import FinanceApi from 'finance/api'
import { areWatchlistsLoaded, areWatchlistsLoading } from 'finance/selectors'

export const KEY = 'loadWatchlists'


export function *maybeLoadWatchlistsSaga() {
  const isLoaded = yield select(areWatchlistsLoaded)
  const isLoading = yield select(areWatchlistsLoading)
  if (!(isLoaded || isLoading)) {
    yield put(loadWatchlists.trigger())
  }
}

export function* loadWatchlistsSaga() {
  try {
    yield put(loadWatchlists.request())
    const watchlists = yield call(FinanceApi.loadWatchlists)
    yield put(loadWatchlists.success({ watchlists }))
  } catch (e) {
    yield put(loadWatchlists.failure(e))
  } finally {
    yield put(loadWatchlists.fulfill())
  }
}

export default () => [
  takeEvery(loadWatchlists.MAYBE_TRIGGER, maybeLoadWatchlistsSaga),
  takeEvery(loadWatchlists.TRIGGER, loadWatchlistsSaga),
]

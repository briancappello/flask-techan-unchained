import { call, put, select, takeEvery } from 'redux-saga/effects'

import { createRoutineSaga } from 'sagas'

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

export const loadWatchlistsSaga = createRoutineSaga(
  loadWatchlists,
  function *() {
    const watchlists = yield call(FinanceApi.loadWatchlists)
    yield put(loadWatchlists.success({ watchlists }))
  }
)

export default () => [
  takeEvery(loadWatchlists.MAYBE_TRIGGER, maybeLoadWatchlistsSaga),
  takeEvery(loadWatchlists.TRIGGER, loadWatchlistsSaga),
]

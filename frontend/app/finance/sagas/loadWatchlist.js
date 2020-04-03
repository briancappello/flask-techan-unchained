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

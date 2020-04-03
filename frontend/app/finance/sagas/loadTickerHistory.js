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

import { call, put, select, takeEvery, takeLatest } from 'redux-saga/effects'
import isString from 'lodash/isString'

import { createRoutineSaga } from 'sagas'

import { loadTickerHistory } from 'finance/actions'
import FinanceApi from 'finance/api'
import { FREQUENCY } from 'finance/constants'
import { hasTickerHistory, isTickerHistoryLoading } from 'finance/reducers/loadTickerHistory'

export const KEY = 'loadTickerHistory'


export function *maybeLoadTickerHistorySaga({ payload: { ticker, frequency } }) {
  const hasTicker = yield select(hasTickerHistory, ticker, frequency)
  const isLoading = yield select(isTickerHistoryLoading, ticker, frequency)
  if (!(hasTicker || isLoading)) {
    yield put(loadTickerHistory.trigger({ ticker, frequency }))
  }
}

export const loadTickerHistorySaga = createRoutineSaga(
  loadTickerHistory,
  function *({ ticker, frequency }) {
    let history = yield call(FinanceApi.loadTickerHistory, ticker, frequency)
    history = parseHistoryJson(history, frequency)
    yield put(loadTickerHistory.success({ ticker, frequency, history }))
  }
)

export default () => [
  takeEvery(loadTickerHistory.MAYBE_TRIGGER, maybeLoadTickerHistorySaga),
  takeLatest(loadTickerHistory.TRIGGER, loadTickerHistorySaga),
]


export function parseHistoryJson(json, frequency) {
  const { columns, data, index } = json
  const dateOnly = [
    FREQUENCY.Daily,
    FREQUENCY.Weekly,
    FREQUENCY.Monthly,
    FREQUENCY.Yearly,
  ].includes(frequency)

  return data.map((values, row_i) => {
    const dt = new Date(index[row_i])
    const row = {
      date: dateOnly
        ? new Date(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate())
        : dt,
    }
    for (let col_i = 0; col_i < values.length; col_i++) {
      // convert empty strings to null, all other values to numbers
      let val = values[col_i]
      val = (val === null || (isString(val) && val.length === 0)) ? null : +val
      row[columns[col_i]] = val
    }
    return row
  })
}

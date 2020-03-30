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

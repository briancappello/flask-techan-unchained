import { call, put, takeLatest } from 'redux-saga/effects'
import { push } from 'redux-first-history'
import { SubmissionError } from 'redux-form'

import { ROUTES, ROUTE_MAP } from 'routes'
import { signUp } from 'security/actions'
import SecurityApi from 'security/api'


export const KEY = 'signUp'

export function* signUpSaga({ payload }) {
  try {
    yield put(signUp.request())
    const { token, user } = yield call(SecurityApi.signUp, payload)
    yield put(signUp.success({ token, user }))
    if (token) {
      yield put(push({
        pathname: ROUTE_MAP[ROUTES.Home].path,
        search: '?welcome',
      }))
    } else {
      yield put(push(ROUTE_MAP[ROUTES.PendingConfirmation].path))
    }
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Sign up failed',
      ...e.response?.errors,
    })
    yield put(signUp.failure(error))
  } finally {
    yield put(signUp.fulfill())
  }
}

export default () => [
  takeLatest(signUp.TRIGGER, signUpSaga),
]

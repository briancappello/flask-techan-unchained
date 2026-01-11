import { call, put, takeLatest } from 'redux-saga/effects'
import { push } from 'redux-first-history'
import { SubmissionError } from 'redux-form'

import { flashSuccess } from 'site/actions'
import { login } from 'security/actions'
import SecurityApi from 'security/api'


export const KEY = 'login'

export function* loginSaga({ payload }) {
  const { redirect, ...credentials } = payload
  try {
    yield put(login.request())
    const { token, user } = yield call(SecurityApi.login, credentials)
    yield put(login.success({ token, user }))
    yield put(push(redirect))
    yield put(flashSuccess('You have been successfully logged in.'))
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Login failed',
      ...e.response?.errors,
    })
    yield put(login.failure(error))
  } finally {
    yield put(login.fulfill())
  }
}

export default () => [
  takeLatest(login.TRIGGER, loginSaga),
]


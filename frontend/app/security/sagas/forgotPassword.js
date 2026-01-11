import { call, put, takeLatest } from 'redux-saga/effects'
import { SubmissionError } from 'redux-form'

import { flashSuccess } from 'site/actions'
import { forgotPassword } from 'security/actions'
import SecurityApi from 'security/api'

export const KEY = 'forgotPassword'

export function* forgotPasswordSaga({ payload }) {
  try {
    yield put(forgotPassword.request())
    yield call(SecurityApi.forgotPassword, payload)
    yield put(forgotPassword.success())
    yield put(
      flashSuccess('A password reset link has been sent to your email address.'),
    )
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Forgot password failed',
      ...e.response?.errors,
    })
    yield put(forgotPassword.failure(error))
  } finally {
    yield put(forgotPassword.fulfill())
  }
}

export default () => [takeLatest(forgotPassword.TRIGGER, forgotPasswordSaga)]

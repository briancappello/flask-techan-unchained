import { call, put, takeLatest } from 'redux-saga/effects'
import { push } from 'redux-first-history'
import { SubmissionError } from 'redux-form'

import { flashSuccess } from 'site/actions'
import { ROUTES, ROUTE_MAP } from 'routes'
import { resetPassword } from 'security/actions'
import SecurityApi from 'security/api'

export const KEY = 'resetPassword'

export function* resetPasswordSaga({ payload }) {
  const { token: resetToken, ...credentials } = payload
  try {
    yield put(resetPassword.request())
    const { token, user } = yield call(
      SecurityApi.resetPassword,
      resetToken,
      credentials,
    )
    yield put(resetPassword.success({ token, user }))
    yield put(push(ROUTE_MAP[ROUTES.Home].path))
    yield put(
      flashSuccess('Welcome back! Your password has been successfully changed.'),
    )
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Reset password failed',
      ...e.response?.errors,
    })
    yield put(resetPassword.failure(error))
  } finally {
    yield put(resetPassword.fulfill())
  }
}

export default () => [takeLatest(resetPassword.TRIGGER, resetPasswordSaga)]

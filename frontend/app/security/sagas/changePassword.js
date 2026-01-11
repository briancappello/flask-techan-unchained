import { call, put, takeLatest } from 'redux-saga/effects'
import { SubmissionError } from 'redux-form'

import { flashSuccess } from 'site/actions'
import { changePassword } from 'security/actions'
import SecurityApi from 'security/api'


export const KEY = 'changePassword'

export function* changePasswordSaga({ payload }) {
  try {
    yield put(changePassword.request())
    const { token } = yield call(SecurityApi.changePassword, payload)
    yield put(changePassword.success({ token }))
    yield put(flashSuccess('Your password has been successfully changed.'))
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Change password failed',
      newPassword: e.response?.errors?.new_password,
      newPasswordConfirm: e.response?.errors?.new_password_confirm,
      ...e.response?.errors,
    })
    yield put(changePassword.failure(error))
  } finally {
    yield put(changePassword.fulfill())
  }
}

export default () => [
  takeLatest(changePassword.TRIGGER, changePasswordSaga),
]

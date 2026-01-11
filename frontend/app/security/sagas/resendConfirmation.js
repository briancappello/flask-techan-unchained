import { call, put, takeLatest } from 'redux-saga/effects'
import { SubmissionError } from 'redux-form'

import { flashSuccess } from 'site/actions'
import { resendConfirmationEmail } from 'security/actions'
import SecurityApi from 'security/api'


export const KEY = 'resendConfirmation'

export function* resendConfirmationEmailSaga({ payload: { email } }) {
  try {
    yield put(resendConfirmationEmail.request())
    yield call(SecurityApi.resendConfirmationEmail, email)
    yield put(resendConfirmationEmail.success())
    yield put(flashSuccess('A new confirmation link has been sent your email address.'))
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Resend confirmation failed',
      ...e.response?.errors,
    })
    yield put(resendConfirmationEmail.failure(error))
  } finally {
    yield put(resendConfirmationEmail.fulfill())
  }
}

export default () => [
  takeLatest(resendConfirmationEmail.TRIGGER, resendConfirmationEmailSaga),
]

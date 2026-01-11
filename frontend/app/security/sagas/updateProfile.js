import { call, put, select, takeLatest } from 'redux-saga/effects'
import { SubmissionError } from 'redux-form'

import { flashClear, flashSuccess } from 'site/actions'
import { updateProfile } from 'security/actions'
import SecurityApi from 'security/api'
import { selectSecurity } from 'security/reducer'

export const KEY = 'updateProfile'

export function* updateProfileSaga({ payload }) {
  try {
    yield put(updateProfile.request())
    yield put(flashClear())
    const { user } = yield select(selectSecurity)
    const updatedUser = yield call(SecurityApi.updateProfile, user, payload)
    yield put(updateProfile.success({ user: updatedUser }))
    yield put(flashSuccess('Your profile has been successfully updated.'))
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Profile update failed',
      ...e.response?.errors,
    })
    yield put(updateProfile.failure(error))
  } finally {
    yield put(updateProfile.fulfill())
  }
}

export default () => [takeLatest(updateProfile.TRIGGER, updateProfileSaga)]

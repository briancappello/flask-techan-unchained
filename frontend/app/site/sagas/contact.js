import { call, put, takeLatest } from 'redux-saga/effects'
import { SubmissionError } from 'redux-form'

import { contact, flashSuccess } from 'site/actions'
import SiteApi from 'site/api'

export const KEY = 'contact'

export function* contactSaga({ payload }) {
  try {
    yield put(contact.request())
    const response = yield call(SiteApi.contact, payload)
    yield put(contact.success(response))
    yield put(
      flashSuccess(
        'Your contact submission has been sent. We will do our best to respond in a timely manner!',
      ),
    )
  } catch (e) {
    const error = new SubmissionError({
      _error: e.response?.error || 'Contact submission failed',
      ...e.response?.errors,
    })
    yield put(contact.failure(error))
  } finally {
    yield put(contact.fulfill())
  }
}

export default () => [takeLatest(contact.TRIGGER, contactSaga)]

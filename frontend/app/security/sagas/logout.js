import { call, put, takeLatest } from 'redux-saga/effects'
import { push } from 'redux-first-history'

import { flashSuccess } from 'site/actions'
import { ROUTES, ROUTE_MAP } from 'routes'
import { logout } from 'security/actions'
import SecurityApi from 'security/api'


export const KEY = 'logout'

export function* logoutSaga() {
  try {
    yield put(logout.request())
    yield call(SecurityApi.logout)
    yield put(logout.success())
    yield put(push(ROUTE_MAP[ROUTES.Home].path))
    yield put(flashSuccess('You have been successfully logged out.'))
  } catch (e) {
    yield put(logout.failure(e))
  } finally {
    yield put(logout.fulfill())
  }
}

export default () => [
  takeLatest(logout.TRIGGER, logoutSaga),
]

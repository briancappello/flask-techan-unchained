import { all, call, put, race, take, takeEvery } from 'redux-saga/effects'

import { ROUTINE_PROMISE } from 'actions'


export function* routineWatcherSaga(action) {
  const { data, routine, defer: { resolve, reject } } = action.payload
  
  try {
    yield put(routine.trigger(data))
    
    const { success, failure } = yield race({
      success: take(routine.SUCCESS),
      failure: take(routine.FAILURE),
    })

    if (success) {
      yield call(resolve, success.payload)
    } else if (failure) {
      yield call(reject, failure.payload)
    }
  } catch (error) {
    if (reject) {
      yield call(reject, error)
    }
  }
}


export default function* rootSaga() {
  yield takeEvery(ROUTINE_PROMISE, routineWatcherSaga)
}

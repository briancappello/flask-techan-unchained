import { call, put, race, take, takeEvery } from 'redux-saga/effects'
import { SubmissionError } from 'redux-form'

import { ROUTINE_PROMISE } from 'actions'


export function createRoutineSaga(routine, successGenerator, failureGenerator) {
  if (!failureGenerator) {
    failureGenerator = function *({ payload, error }) {
      if (!error.response) {
        // something unexpected went wrong, probably in the successGenerator fn
        throw error
      }
      yield put(routine.failure({ ...payload, ...error.response }))
    }
  }
  return function *({ payload }) {
    try {
      yield put(routine.request())
      yield successGenerator(payload)
    } catch (error) {
      yield failureGenerator({ payload, error})
    } finally {
      yield put(routine.fulfill(payload))
    }
  }
}


export function createRoutineFormSaga(routine, successGenerator, renames) {
  return createRoutineSaga(routine, successGenerator, function *onError(e) {
    if (!e.response) {
      // something unexpected went wrong, probably in the successGenerator fn
      throw e
    }

    const error = new SubmissionError(Object.assign(
      { _error: e.response.error || null },
      renameKeys(e.response.errors, renames) || {},
    ))

    yield put(routine.failure(error))
  })
}


export function *routineWatcherSaga({ payload }) {
  const { data, routine, defer: { resolve, reject } } = payload
  const [{ success, failure }] = yield [
    race({
      success: take(routine.SUCCESS),
      failure: take(routine.FAILURE),
    }),
    put(routine.trigger(data)),
  ]

  if (success) {
    yield call(resolve)
  } else {
    yield call(reject, failure && failure.payload || failure)
  }
}


function renameKeys(obj, renames) {
  if (!renames || !obj) {
    return obj
  }

  return Object.keys(obj).reduce((newObj, key) => {
    newObj[renames[key] || key] = obj[key]
    return newObj
  }, {})
}


export default () => [
  takeEvery(ROUTINE_PROMISE, routineWatcherSaga),
]

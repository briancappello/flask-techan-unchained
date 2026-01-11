import { flashClear } from 'site/actions'
import { LOCATION_CHANGE } from 'redux-first-history'


export const flashClearMiddleware = ({ getState, dispatch }) => (next) => (action) => {
  if (action.type == LOCATION_CHANGE && getState().flash.visible) {
    dispatch(flashClear())
  }
  return next(action)
}

import { flashClear } from 'site/actions'
import { LOCATION_CHANGE } from 'redux-first-history'


export const flashClearMiddleware = ({ getState, dispatch }) => (next) => (action) => {
  if (action.type === LOCATION_CHANGE && getState().flash.visible) {
    if (action.payload?.location?.pathname === getState().router.location?.pathname) {
      return next(action)
    }
    dispatch(flashClear())
  }
  return next(action)
}

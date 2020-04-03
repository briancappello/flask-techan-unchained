import { combineReducers } from 'redux'
import formReducer from 'redux-form/es/reducer'
import { routerReducer } from 'react-router-redux'
import { loadingBarReducer } from 'react-redux-loading-bar'

import securityReducer from 'security/reducer'
import flashReducer from 'site/reducers/flash'
import financeReducer from 'finance/reducers'

export default function createReducer(injectedReducers) {
  return combineReducers({
    security: securityReducer,
    flash: flashReducer,
    finance: financeReducer,

    form: formReducer,
    routing: routerReducer,
    loadingBar: loadingBarReducer,

    ...injectedReducers,
  })
}

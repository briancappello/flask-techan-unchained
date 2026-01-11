import { combineReducers } from 'redux'
import { reducer as formReducer } from 'redux-form'
import { loadingBarReducer } from 'react-redux-loading-bar'

import securityReducer from 'security/reducer'
import flashReducer from 'site/reducers/flash'
import financeReducer from 'finance/reducers'

export default function createReducer(routerReducer, injectedReducers) {
  return combineReducers({
    security: securityReducer,
    flash: flashReducer,
    finance: financeReducer,

    form: formReducer,
    router: routerReducer,
    loadingBar: loadingBarReducer,

    ...injectedReducers,
  })
}

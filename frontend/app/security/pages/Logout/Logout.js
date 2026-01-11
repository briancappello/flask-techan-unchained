import React, { useEffect } from 'react'
import { compose } from 'redux'
import { useDispatch } from 'react-redux'

import { logout } from 'security/actions'
import { injectSagas } from 'utils/async'
import * as logoutSagas from 'security/sagas/logout'


const Logout = () => {
  const dispatch = useDispatch()
  
  useEffect(() => {
    dispatch(logout.trigger())
  }, [dispatch])

  return null
}

const withSagas = injectSagas(logoutSagas)

export default compose(
  withSagas,
)(Logout)

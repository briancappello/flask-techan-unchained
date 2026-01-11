import React, { useEffect } from 'react'
import { useDispatch } from 'react-redux'

import { PageContent } from 'components'
import { logout } from 'security/actions'
import { injectSagas } from 'utils/async'
import * as logoutSagas from 'security/sagas/logout'

const Logout = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(logout.trigger())
  }, [dispatch])

  // return
  return (
    <PageContent>
      <p>Logging out...</p>
    </PageContent>
  )
}

const withSagas = injectSagas(logoutSagas)

export default withSagas(Logout)

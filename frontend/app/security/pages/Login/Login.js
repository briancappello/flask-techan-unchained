import React from 'react'
import { Helmet } from 'react-helmet-async'
import { compose } from 'redux'
import { connect } from 'react-redux'
import { reduxForm } from 'redux-form'
import { useSearchParams } from 'react-router-dom'

import { login } from 'security/actions'
import { DangerAlert, PageContent } from 'components'
import { NavLink } from 'components/Nav'
import { HiddenField, PasswordField, TextField } from 'components/Form'
import { ROUTES } from 'routes'
import { injectSagas } from 'utils/async'
import * as loginSagas from 'security/sagas/login'


const FORM_NAME = 'login'

const Login = (props) => {
  const isDev = import.meta.env.MODE !== 'production'
  const { error, handleSubmit, submitting, pristine } = props
  const [searchParams] = useSearchParams()
  const redirect = searchParams.get('next') || '/'

  return (
    <PageContent>
      <Helmet>
        <title>Login</title>
      </Helmet>
      <div className="row">
        <div className="six cols offset-by-three">
          <h1>Log in!</h1>
          {error && <DangerAlert>{error}</DangerAlert>}
          {isDev && <p>Hint: a@a.com / password</p>}
          <form onSubmit={handleSubmit((values) => login({ ...values, redirect }))}>
            <TextField name="email"
                       label="Email or Username"
                       className="full-width"
                       autoFocus
            />
            <PasswordField name="password"
                           className="full-width"
            />
            <div className="row">
              <button type="submit"
                      className="btn btn-primary"
                      disabled={pristine || submitting}
              >
                {submitting ? 'Logging in...' : 'Submit'}
              </button>
              <NavLink to={ROUTES.ForgotPassword}
                       className="pull-right"
                       style={{lineHeight: '38px'}}
              />
            </div>
          </form>
        </div>
      </div>
    </PageContent>
  )
}

const withForm = reduxForm({ form: FORM_NAME })

const withSagas = injectSagas(loginSagas)

export default compose(
  withForm,
  withSagas,
)(Login)

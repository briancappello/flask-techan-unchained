import React from 'react'
import { compose } from 'redux'
import { Helmet } from 'react-helmet-async'
import { reduxForm, reset } from 'redux-form'

import { forgotPassword } from 'security/actions'
import { DangerAlert } from 'components/Alert'
import { PageContent } from 'components/Content'
import { EmailField } from 'components/Form'
import { injectSagas } from 'utils/async'
import * as forgotPasswordSagas from 'security/sagas/forgotPassword'


const FORM_NAME = 'forgotPassword'

const ForgotPassword = (props) => {
  const { error, handleSubmit, submitting, pristine } = props
  return (
    <PageContent>
      <Helmet>
        <title>Forgot Password</title>
      </Helmet>
      <div className="row">
        <div className="six cols offset-by-three">
          <h1>Forgot Password</h1>
          {error && <DangerAlert>{error}</DangerAlert>}
          <form onSubmit={handleSubmit(forgotPassword)}>
            <EmailField name="email"
                        label="Email Address"
                        className="full-width"
                        autoFocus
            />
            <div className="row">
              <button type="submit"
                      className="btn btn-primary"
                      disabled={pristine || submitting}
              >
                {submitting ? 'Submitting...' : 'Submit'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </PageContent>
  )
}

const withForm = reduxForm({
  form: FORM_NAME,
  onSubmitSuccess: (_, dispatch) => {
    dispatch(reset(FORM_NAME))
  },
})

const withSagas = injectSagas(forgotPasswordSagas)

export default compose(
  withForm,
  withSagas,
)(ForgotPassword)

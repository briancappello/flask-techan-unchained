import React from 'react'
import { compose } from 'redux'
import { reduxForm } from 'redux-form'
import { Helmet } from 'react-helmet-async'
import { useParams } from 'react-router-dom'

import { resetPassword } from 'security/actions'
import { DangerAlert } from 'components/Alert'
import { PageContent } from 'components/Content'
import { PasswordField } from 'components/Form'
import { injectSagas } from 'utils/async'
import * as resetPasswordSagas from 'security/sagas/resetPassword'

const FORM_NAME = 'resetPassword'

const ResetPassword = (props) => {
  const { error, handleSubmit, pristine, submitting } = props
  const { token } = useParams()

  return (
    <PageContent>
      <Helmet>
        <title>Reset Password</title>
      </Helmet>
      <h1>Reset Password</h1>
      {error && <DangerAlert>{error}</DangerAlert>}
      <p>Enter a new password and click submit to reset your password and login.</p>
      <form
        onSubmit={handleSubmit((values, dispatch) =>
          resetPassword({ ...values, token }, dispatch),
        )}
      >
        <PasswordField name="newPassword" autoFocus />
        <PasswordField name="confirmNewPassword" label="Confirm New Password" />
        <div className="row">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={pristine || submitting}
          >
            {submitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </form>
    </PageContent>
  )
}

const withForm = reduxForm({ form: FORM_NAME })

const withSagas = injectSagas(resetPasswordSagas)

export default compose(withForm, withSagas)(ResetPassword)

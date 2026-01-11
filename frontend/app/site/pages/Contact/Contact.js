import React from 'react'
import { Helmet } from 'react-helmet-async'
import { compose } from 'redux'
import { connect } from 'react-redux'
import { reduxForm, reset } from 'redux-form'

import { contact } from 'site/actions'
import { DangerAlert, PageContent } from 'components'
import { EmailField, TextArea, TextField } from 'components/Form'
import { injectSagas } from 'utils/async'
import * as contactSagas from 'site/sagas/contact'

const FORM_NAME = 'contact'

const Contact = (props) => {
  const { error, handleSubmit, pristine, submitting } = props

  return (
    <PageContent>
      <Helmet>
        <title>Contact</title>
      </Helmet>
      <h1>Contact!</h1>
      {error && <DangerAlert>{error}</DangerAlert>}
      <form onSubmit={handleSubmit(contact)}>
        <div className="row">
          <div className="six cols">
            <TextField name="name" label="Name" className="full-width" autoFocus />
          </div>
          <div className="six cols">
            <EmailField name="email" className="full-width" />
          </div>
        </div>
        <TextArea name="message" className="full-width" rows="6" />
        <div className="row">
          <button
            type="submit"
            className="button-primary"
            disabled={pristine || submitting}
          >
            {submitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </form>
    </PageContent>
  )
}

const withConnect = connect((state) =>
  state.security.isAuthenticated
    ? { initialValues: { email: state.security.user.email } }
    : {},
)

const withForm = reduxForm({
  form: FORM_NAME,
  onSubmitSuccess: (_, dispatch) => {
    dispatch(reset(FORM_NAME))
  },
})

const withSaga = injectSagas(contactSagas)

export default compose(withConnect, withForm, withSaga)(Contact)

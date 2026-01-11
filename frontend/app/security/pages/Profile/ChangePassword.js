import React, { useState, useEffect } from 'react'
import { compose } from 'redux'
import { useDispatch } from 'react-redux'
import { reduxForm, reset } from 'redux-form'

import { changePassword } from 'security/actions'
import { DangerAlert } from 'components/Alert'
import { PasswordField } from 'components/Form'
import { injectSagas } from 'utils/async'
import * as changePasswordSagas from 'security/sagas/changePassword'


const FORM_NAME = 'changePassword'

const ChangePassword = (props) => {
  const { error, handleSubmit, pristine, submitting, submitSucceeded } = props
  const [formVisible, setFormVisible] = useState(false)
  const dispatch = useDispatch()

  useEffect(() => {
    if (submitSucceeded) {
      setFormVisible(false)
      dispatch(reset(FORM_NAME))
    }
  }, [submitSucceeded, dispatch])

  const renderShowFormButton = () => (
    <button type="button"
            className="btn"
            onClick={() => setFormVisible(true)}
    >
      Click to change your password
    </button>
  )

  const renderForm = () => (
    <div>
      {error && <DangerAlert>{error}</DangerAlert>}
      <form onSubmit={handleSubmit(changePassword)}>
        <PasswordField name="password"
                       label="Current Password"
                       autoFocus
        />
        <PasswordField name="newPassword"
                       label="New Password"
        />
        <PasswordField name="confirmNewPassword"
                       label="Confirm New Password"
        />
        <div className="row">
          <button type="submit"
                  className="btn btn-primary"
                  disabled={pristine || submitting}
          >
            {submitting ? 'Saving...' : 'Save'}
          </button>
          {' '}
          <button type="button"
                  className="btn"
                  onClick={() => {
                    setFormVisible(false)
                    dispatch(reset(FORM_NAME))
                  }}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )

  return (
    <div>
      <h2>Change Password!</h2>
      {formVisible ? renderForm() : renderShowFormButton()}
    </div>
  )
}

const withForm = reduxForm({ form: FORM_NAME })

const withSagas = injectSagas(changePasswordSagas)

export default compose(
  withForm,
  withSagas,
)(ChangePassword)

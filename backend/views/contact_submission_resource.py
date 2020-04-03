# Flask Techan Unchained
#
# Copyright (C) 2020  Brian Cappello
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import current_app

from flask_unchained.bundles.api import ModelResource
from flask_unchained.bundles.mail import Mail
from flask_unchained import injectable

from ..models import ContactSubmission


class ContactSubmissionResource(ModelResource):
    class Meta:
        model = ContactSubmission
        include_methods = ('create',)

    def __init__(self, mail: Mail = injectable):
        super().__init__()
        self.mail = mail

    def create(self, contact_submission, errors):
        if errors:
            return self.errors(errors)

        self.mail.send(subject='New Contact Submission',
                       to=current_app.config.get('MAIL_ADMINS'),
                       template='email/new_contact_submission.html',
                       contact_submission=contact_submission)

        return self.created(contact_submission)

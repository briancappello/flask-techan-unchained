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

import html
import re

from flask_unchained.bundles.api import ma
from backend.models import ContactSubmission


class ContactSubmissionSerializer(ma.ModelSerializer):
    class Meta:
        model = ContactSubmission

    email = ma.Email(required=True)

    @ma.pre_load
    def message_to_html(self, data):
        if not data.get('message'):
            return None
        message = html.escape(data['message'])
        message = re.sub(r'\n\n+', '\n\n', '\n'.join(map(
            str.strip,
            message.splitlines()
        )))
        data['message'] = '\n'.join(map(
            lambda p: f'<p>{p!s}</p>',
            message.splitlines()
        ))
        return data

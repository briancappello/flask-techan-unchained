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

from flask_unchained.bundles.admin import ModelAdmin, macro

from ..models import ContactSubmission


class ContactSubmissionAdmin(ModelAdmin):
    model = ContactSubmission

    name = 'Contact Submissions'
    category_name = 'Mail'
    menu_icon_value = 'glyphicon-envelope'

    can_create = False
    can_edit = False

    column_list = ('name', 'email', 'message', 'created_at')
    column_exclude_list = ('updated_at',)
    column_labels = {'created_at': 'Date'}
    column_default_sort = ('created_at', True)

    column_details_list = ('name', 'email', 'message', 'created_at')

    column_formatters = {
        'email': macro('column_formatters.email'),
        'message': macro('column_formatters.safe'),
    }

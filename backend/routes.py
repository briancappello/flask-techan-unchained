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

from flask_unchained import (
    controller, func, get, include, patch, post, prefix, put, resource, rule)
from flask_unchained.bundles.security import SecurityController, UserResource

from backend.views import ContactSubmissionResource
from bundles.finance.views import HistoryController, WatchlistResource

routes = lambda: [
    controller('/auth', SecurityController, rules=[
        get('/confirm/<token>', SecurityController.confirm_email),
        get('/reset-password/<token>', SecurityController.reset_password),
    ]),

    prefix('/api/v1', [
        controller('/auth', SecurityController, rules=[
            get('/check-auth-token', SecurityController.check_auth_token, only_if=True),
            post('/login', SecurityController.login),
            get('/logout', SecurityController.logout),
            post('/send-confirmation-email', SecurityController.send_confirmation_email),
            post('/forgot-password', SecurityController.forgot_password),
            post('/reset-password/<token>', SecurityController.reset_password,
                 endpoint='security.post_reset_password'),
            post('/change-password', SecurityController.change_password),
        ]),

        resource('/users', UserResource),

        resource('/contact-submissions', ContactSubmissionResource),

        prefix('/finance', [
            controller('/', HistoryController),
            resource('/watchlists', WatchlistResource),
        ]),
    ]),

    # frontend routes
    get('/', endpoint='frontend.index'),
    get('/login/forgot-password', endpoint='frontend.forgot_password'),
    get('/login/reset-password/<token>', endpoint='frontend.reset_password'),
    get('/sign-up/resend-confirmation-email',
        endpoint='frontend.resend_confirmation_email'),
]

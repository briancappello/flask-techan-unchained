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

from flask_unchained import AppBundle, FlaskUnchained, generate_csrf, session


class App(AppBundle):
    def before_init_app(self, app: FlaskUnchained) -> None:
        app.url_map.strict_slashes = False

    def after_init_app(self, app: FlaskUnchained):
        app.jinja_env.add_extension('jinja2_time.TimeExtension')

        # set session to use PERMANENT_SESSION_LIFETIME
        # and reset the session timer on every request
        @app.before_request
        def enable_session_timeout():
            session.permanent = True
            session.modified = True

        # send CSRF token in the cookie
        @app.after_request
        def set_csrf_cookie(response):
            if response:
                response.set_cookie('csrf_token', generate_csrf())
            return response

# Flask Techan Unchained
#
# Copyright 2019 Brian Cappello
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, session
from flask_unchained import AppBundle as BaseAppBundle


class AppBundle(BaseAppBundle):
    @classmethod
    def before_init_app(cls, app: Flask):
        app.url_map.strict_slashes = False

    @classmethod
    def after_init_app(cls, app: Flask):
        app.jinja_env.add_extension('jinja2_time.TimeExtension')

        # set session to use PERMANENT_SESSION_LIFETIME
        # and reset the session timer on every request
        @app.before_request
        def enable_session_timeout():
            session.permanent = True
            session.modified = True

        for rule in app.url_map.iter_rules():
            if 'static' in rule.endpoint:
                rule.strict_slashes = True
            else:
                rule.strict_slashes = False

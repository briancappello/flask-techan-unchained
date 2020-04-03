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

import os

from flask_unchained import AppFactory, PROD

# we import this here so celery can access it for its startup
from flask_unchained.bundles.celery import celery  # NOQA


app = AppFactory.create_app(os.getenv('FLASK_ENV', PROD))
app.app_context().push()

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

project_root = os.path.abspath(os.path.dirname(__file__))


def folder_or_none(folder_name):
    if not os.path.exists(os.path.join(project_root, folder_name)):
        return None
    return folder_name


# these get passed to the Flask constructor
TEMPLATE_FOLDER = folder_or_none('templates')
STATIC_FOLDER = folder_or_none('static')
STATIC_URL_PATH = '/static' if STATIC_FOLDER else None

BUNDLES = [
    'flask_unchained.bundles.api',
    'flask_unchained.bundles.mail',
    'flask_unchained.bundles.celery',
    'flask_unchained.bundles.session',
    'flask_unchained.bundles.sqlalchemy',
    'py_yaml_fixtures',

    'bundles.finance',
    'bundles.security',
    'backend',
]

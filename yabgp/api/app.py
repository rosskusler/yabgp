# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Set up the API server application instance
"""

import flask

from yabgp.api import v1
from yabgp.api import config
from oslo.config import cfg

app = flask.Flask('yabgp.api')
app.register_blueprint(v1.blueprint, url_prefix='/v1')

cfg.CONF.register_cli_opts(config.rest_server_ops, group='rest')


@app.route('/')
def index():

    base_url = flask.request.base_url
    available = [
        {'tag': 'v1'}]
    collected = [version_descriptor(base_url, v['tag']) for v in available]
    versions = {'versions': {'values': collected}}
    print versions
    return flask.jsonify(versions)


def version_descriptor(base_url, version):
    url = version_url(base_url, version)
    return {
        'id': version,
        'links': url,
        'status': 'stable'
    }


def version_url(base_url, version_number):
    return '%s/%s' % (base_url, version_number)

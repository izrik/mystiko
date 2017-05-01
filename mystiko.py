#!/usr/bin/env python3

# mystiko - A host-proof web application for storing secrets.
# Copyright (C) 2016-2017 izrik
#
# This file is a part of mystiko.
#
# Mystiko is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mystiko is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with mystiko.  If not, see <http://www.gnu.org/licenses/>.


import argparse
from os import environ

import git
from flask import Flask

__version_tuple__ = (0, 1)
__version__ = '.'.join(str(i) for i in __version_tuple__)

try:
    __revision__ = git.Repo('.').git.describe(tags=True, dirty=True,
                                              always=True, abbrev=40)
except git.InvalidGitRepositoryError:
    __revision__ = 'unknown'


class Config(object):
    DEBUG = environ.get('MYSTIKO_DEBUG', False)
    PORT = environ.get('MYSTIKO_PORT', 5352)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='',
                        default=Config.DEBUG)
    parser.add_argument('--port', type=int, default=Config.PORT,
                        help='')

    args = parser.parse_args()

    Config.DEBUG = args.debug

app = Flask(__name__)


@app.route("/")
def index():
    return '', 200


def run():
    print('Mystiko {}'.format(__version__))
    print('  Revision {}'.format(__revision__))
    print('  Debug: {}'.format(Config.DEBUG))
    print('  Port: {}'.format(Config.PORT))

    app.run(debug=Config.DEBUG, port=Config.PORT,
            use_reloader=Config.DEBUG)


if __name__ == "__main__":
    run()

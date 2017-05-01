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


class Config(object):
    DEBUG = environ.get('MYSTIKO_DEBUG', False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='',
                        default=Config.DEBUG)

    args = parser.parse_args()

    Config.DEBUG = args.debug


def run():
    print('Mystiko')
    print('  Debug: {}'.format(Config.DEBUG))


if __name__ == "__main__":
    run()

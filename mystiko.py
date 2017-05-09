#!/usr/bin/env python

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
from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_uuid import FlaskUUID
from werkzeug.exceptions import NotFound

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
    DB_URI = environ.get('MYSTIKO_DB_URI', 'sqlite:////tmp/blog.db')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='',
                        default=Config.DEBUG)
    parser.add_argument('--port', type=int, default=Config.PORT,
                        help='')
    parser.add_argument('--db-uri', type=str, action='store',
                        default=Config.DB_URI)

    parser.add_argument('--create-db', action='store_true')

    args = parser.parse_args()

    Config.DEBUG = args.debug
    Config.PORT = args.port
    Config.DB_URI = args.db_uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URI
FlaskUUID(app)

db = SQLAlchemy(app)
app.db = db


class Item(db.Model):
    item_id = db.Column(db.String(38), primary_key=True)
    content = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, item_id, content):
        self.item_id = item_id
        self.content = bytes(content)


@app.route("/")
def index():
    return '', 200


@app.route("/item/<uuid:item_id>", methods=['GET'])
def get_item(item_id):
    id_str = str(item_id)
    item = Item.query.get(id_str)
    content = ''
    if item is not None:
        content = item.content
    return make_response(content, 200)


@app.route("/item/<uuid:item_id>", methods=['POST'])
def set_item(item_id):
    id_str = str(item_id)
    content = request.get_data()
    item = Item.query.get(id_str)
    if item is None:
        item = Item(id_str, content)
    else:
        item.content = content
    db.session.add(item)
    db.session.commit()
    return '', 204


def create_db():
    db.create_all()


def run():
    print('Mystiko {}'.format(__version__))
    print('  Revision {}'.format(__revision__))
    print('  Debug: {}'.format(Config.DEBUG))
    print('  Port: {}'.format(Config.PORT))
    if Config.DEBUG:
        print('  DB URI: {}'.format(Config.DB_URI))

    if args.create_db:
        print('Setting up the database')
        create_db()
    else:
        app.run(debug=Config.DEBUG, port=Config.PORT,
                use_reloader=Config.DEBUG)


if __name__ == "__main__":
    run()

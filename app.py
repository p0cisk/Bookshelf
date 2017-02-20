#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from peewee import SqliteDatabase

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('local_config')

db = SqliteDatabase(app.config['DBPATH'])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)

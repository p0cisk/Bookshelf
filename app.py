#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from peewee import OperationalError
from models import db, Books, Magazines, Stories, Authors, Files
import os

#Initialize flask application
app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('local_config')

#Initialize databse
db.init( app.config['DBPATH'] )
if not os.path.exists( app.config['DBPATH'] ):
    #Create db if not exist
    try:
        db.create_tables( [Books, Magazines, Stories, Authors, Files] )
    except OperationalError:
        pass

if __name__ == '__main__':
    #Run flask server
    app.run(host='0.0.0.0', port=6000)

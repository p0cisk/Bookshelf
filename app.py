#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from peewee import OperationalError
from models import db, Books, Stories, Authors, Files
import os

#Initialize flask application
app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('local_config')

#Routings
from routings import mod_routings
app.register_blueprint(mod_routings)

#Initialize databse
db.init( app.config['DBPATH'] )
if not os.path.exists( app.config['DBPATH'] ):
    #Create db if not exist
    try:
        db.create_tables( [Books, Stories, Authors, Files] )
        try:
            #Add sample data
            from add_sample import add_sample
            add_sample()
        except:
            pass
    except OperationalError:
        pass

if __name__ == '__main__':
    #Run flask server
    app.run(host='0.0.0.0', port=5000)

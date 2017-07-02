#!/usr/bin/python
# -*- coding: utf-8 -*-

from peewee import SqliteDatabase, Model, TextField, BlobField, IntegerField, \
    ForeignKeyField
from playhouse.sqlite_ext import JSONField

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class Files(BaseModel):
    filename = TextField()
    content = BlobField()

class Authors(BaseModel):
    first_name = TextField()
    second_name = TextField()

class Books(BaseModel):
    title = TextField()
    file_content = ForeignKeyField(Files, related_name='book_files', null=True)
    links = JSONField(null=True)
    year = IntegerField(null=True)
    #magazines
    number = IntegerField(null=True)
    number_year = IntegerField(null=True)

class Stories(BaseModel):
    title = TextField()
    author = ForeignKeyField(Authors, related_name='story_authors')
    book = ForeignKeyField(Books, related_name='story_books')
    year = IntegerField(null=True)

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
    name = TextField()
    surname = TextField()

class Stories(BaseModel):
    title = TextField()
    author = ForeignKeyField(Authors, related_name='story_authors')

class Magazines(BaseModel):
    title = TextField()
    number = IntegerField(null=True)
    number_year = IntegerField(null=True)
    year = IntegerField(null=True)
    stories = ForeignKeyField(Stories, related_name='magazine_stories', null=True)
    file_content = ForeignKeyField(Files, related_name='magazine_files', null=True)

class Books(BaseModel):
    title = TextField()
    author = ForeignKeyField(Authors, related_name='books_authors', null=True)
    file_content = ForeignKeyField(Files, related_name='book_files', null=True)
    stories = ForeignKeyField(Stories, related_name='book_stories', null=True)
    links = JSONField(null=True)

#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, redirect
from models import Books, Authors, Stories
from peewee import fn
from playhouse.test_utils import  count_queries

mod_routings = Blueprint('routings', __name__)

#PAGES

@mod_routings.route('/')
def index():
    return redirect('books')

@mod_routings.route('/books')
def books():
    return render_template('books.html')

@mod_routings.route('/authors')
def authors():
    return render_template('authors.html')

# API

@mod_routings.route('/api/books')
def api_books():
    with count_queries() as counter:
        rs = (Books.select(Books, Stories, Authors)
            .join(Stories)
            .join(Authors)
            .aggregate_rows()
            )
        result = []
        for row in rs:
            book = {'title':row.title}
            authors = {}
            for story in row.story_books:
                author = story.author
                authors[author.id] = '{}, {}'.format(author.second_name, author.first_name)
            book_authors = []
            for aid, author in authors.items():
                book_authors.append({'id':aid, 'name':author})
            book['authors'] = book_authors
            result.append( book )
    print (counter.count)
    return jsonify({'result':result})

@mod_routings.route('/api/authors')
def api_authors():
    rs = Authors.select().order_by(Authors.second_name, Authors.first_name).dicts()
    return jsonify({'result':list(rs)})

@mod_routings.route('/api/authors/<int:id>')
def api_author(id):
    rs = Authors.select().where(Authors.id==id).dicts().get()
    return jsonify(rs)

@mod_routings.route('/api/authors_books/<int:id>')
def api_author_books(id):
    books_id = set(Stories.select(fn.Distinct(Stories.book)).where(Stories.author==id).tuples())
    rs = Books.select().where(Books.id<<books_id).dicts()
    return jsonify({'result':list(rs)})

@mod_routings.route('/api/authors_stories/<int:id>')
def api_author_stories(id):
    rs = Stories.select().where(Stories.author==id).dicts()
    return jsonify({'result':list(rs)})

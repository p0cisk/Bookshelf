#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, redirect
from models import Books, Authors, Stories
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
    #print (counter.get_queries())
    #print (dir(counter))
    return jsonify({'result':result})


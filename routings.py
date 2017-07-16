#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, render_template, redirect, request
from models import Books, Authors, Stories, AuthorsStories
from peewee import fn
from decorators import count
from playhouse.shortcuts import model_to_dict
from collections import defaultdict

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

@mod_routings.route('/authors/<int:aid>')
def authors_id(aid):
    return render_template('authors_id.html', aid=aid)

# API

@mod_routings.route('/api/books')
@count
def api_books():
    #TODO: Fix when needed
    result = []
    
    #B = Books.select()
    #S = Stories.select()
    rs = Stories.select(Stories, Authors).join(AuthorsStories).join(Authors).aggregate_rows()
    for row in rs:
        print(row)
    print(dir(row))
    
    
    """
    rs = (Books.select(Books, Stories, Authors)
        .join(Stories)
        .join(AuthorsStories)
        .join(Authors)
        .aggregate_rows()
        )
    print( rs)
    
    for row in rs:
        #print (row)
        #print (row.story_books)
        #print (dir(row.story_books[0]))
        #print (model_to_dict(row))
        
        #book = {'title':row.title}
        book = model_to_dict(row)#{'title':row.title}
        authors = {}
        #for story in row.story_books:
        #    print (story)
        #    print (list(story.authorsstories_set))
        '''
        authors = {}
        for story in row.story_books:
            print (story)
            print (story.authorsstories_set)
            print (dir(story.authorsstories_set))
            author = story.author
            authors[author.id] = '{}, {}'.format(author.second_name, author.first_name)
        book_authors = []
        for aid, author in authors.items():
            book_authors.append({'id':aid, 'name':author})
        book['authors'] = book_authors'''
        result.append( book )
        
        '''
        book = {'title':row.title}
        authors = {}
        for story in row.story_books:
            print (story)
            print (story.authorsstories_set)
            print (dir(story.authorsstories_set))
            author = story.author
            authors[author.id] = '{}, {}'.format(author.second_name, author.first_name)
        book_authors = []
        for aid, author in authors.items():
            book_authors.append({'id':aid, 'name':author})
        book['authors'] = book_authors
        result.append( book )
        '''
    """
    return jsonify({'result':result})

@mod_routings.route('/api/authors', methods=['GET', 'POST'])
def api_authors():
    if request.method=='GET':
        rs = Authors.select().order_by(Authors.second_name, Authors.first_name).dicts()
        return jsonify({'result':list(rs)})
    else:
        rs = Authors.create(**request.get_json(force=True))
        return jsonify(model_to_dict(rs))

@mod_routings.route('/api/authors/<int:aid>', methods=['GET', 'PUT'])
def api_author(aid):
    if request.method=='GET':
        rs = Authors.select().where(Authors.id==aid).dicts().get()
        return jsonify(rs)
    else:
        data = request.get_json(force=True)
        rs = Authors.update(**data).where(Authors.id==aid).execute()
        return jsonify(data)

@mod_routings.route('/api/authors_books/<int:aid>')
def api_author_books(aid):
    books_id = set(Stories.select(fn.Distinct(Stories.book)).where(Stories.author==aid).tuples())
    rs = Books.select().where(Books.id<<books_id).dicts()
    return jsonify({'result':list(rs)})

@mod_routings.route('/api/authors_stories/<int:aid>')
def api_author_stories(aid):
    rs = Stories.select().join(AuthorsStories).where(AuthorsStories.author==aid).dicts()
    return jsonify({'result':list(rs)})

@mod_routings.route('/api/stories')
@count
def api_stories():
    result = []
    rs = (AuthorsStories
        .select(AuthorsStories, Stories, Authors)
        .join(Stories)
        .switch(AuthorsStories)
        .join(Authors)
        )
    stories = defaultdict(lambda:defaultdict(dict))
    for row in rs:
        stories[row.story.id]['authors'][row.author.id] = model_to_dict(row.author)
        stories[row.story.id]['title'] = row.story.title
        stories[row.story.id]['id'] = row.story.id
    for story in stories.values():
        story['authors'] = list(story['authors'].values())
        result.append(story)
    return jsonify({'result':result})

@mod_routings.route('/api/stories/<int:aid>')
@count
def api_stories_by_id(aid):
    story = Stories.select().where(Stories.id==aid).dicts().get()
    story['authors'] = list(Authors
        .select()
        .join(AuthorsStories)
        .join(Stories)
        .where(Stories.id==aid)
        .dicts()
        )
    return jsonify({'result':story})

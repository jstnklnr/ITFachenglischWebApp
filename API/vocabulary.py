from flask_restful import Resource
from flask_restful import reqparse
from flask import Flask, request
from main import db

import random

class Vocabulary(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("books", type = str)
        self.reqparse.add_argument("topics", type = str)
        self.reqparse.add_argument("units", type = str)
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        args = self.reqparse.parse_args()

        #parameter missing
        if not args['books']:
            return {"Error": "Books is missing."}, 400
        if not args['amount']:
            return {"Error": "Amount is missing."}, 400
        if not args['lang']:
            return {"Error": "Language is missing."}, 400
        if ',' in args['books']:
            if args['units']:
                return {"Error": "Can't use units for more then one book."}, 400
            if not args['topics']:
                return {"Error": "Topic is missing."}, 400
        else:
           if not args['units']:
                return {"Error": "Unit is missing."}, 400
        if  args['topics']:
                return {"Error": "Can't use topics for only one book."}, 400 
                
        #amount not acceptable
        if args['amount'] > 100:
            return {"Error": "Amount is to high."}, 403
        if args['amount'] < 1:
            return {"Error": "Amount is to low."}, 403


        #SQL WHERE Languages
        langs = args['languages'].split(',')
        langsStr = ""
        langsList = []
        for i in range(langs):
            langsStr += "languages.language = ?"
            langsList.append(langs[i])

            if i != len(topics) - 1:
                langsStr += " OR "


        #SQL QUERYS
        resultList = None
        if args['topic']:
            books = args['books'].split(',')
            topics = args['topics'].split(',')

            #SQL Where Books
            bookStr = ""
            bookList = []
            for i in range(books):
                bookStr += "books.book = ?"
                bookList.append(books[i])

                if i != len(books) - 1:
                    bookStr += " OR "
            
            #SQL WHERE Topics
            topicStr = ""
            topicList = []
            for i in range(topics):
                topicStr += "or topics.topic = ?"
                topicList.append(topics[i])

                if i != len(topics) - 1:
                    topicStr += " OR "

            resultList = db.query_dict(f"""
                                    SELECT vocabulary.word, vocabulary.translation 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN topics ON topics.id = vocabulary.topic
                                    WHERE ({bookStr}) AND ({topicStr}) AND ({langsStr})
                                    ORDER BY random() LIMIT ?
                                    """, tuple(bookList + topicList + langsList + [args['amount']]))
        else:
            units = args['units'].split(',')  

            unitStr = ""
            unitList = []
            for i in range(units):
                unitStr += "books.book = ?"
                unitList.append(units[i])

                if i != len(units) - 1:
                    unitStr += " OR "

            resultList = db.query_dict(f"""
                                    SELECT vocabulary.word, vocabulary.translation 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN units ON units.id = vocabulary.unit
                                    WHERE ({unitStr}) AND ({langsStr}) 
                                    ORDER BY random() LIMIT ?
                                    """, tuple(unitList + langsList + [args['amount']]))
        return resultList, 200

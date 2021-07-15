from flask_restful import Resource
from flask_restful import reqparse
from flask import Flask, request
import random
import static

class Vocabulary(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("books", type = str)
        self.reqparse.add_argument("topics", type = str)
        self.reqparse.add_argument("units", type = str)
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        db = static.database
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
        if args["amount"] and args['amount'] < 1:
            return {"Error": "Amount is to low."}, 403


        #SQL WHERE Languages
        langs = args['languages'].split(',')
        langs_str = ""
        langs_list = []
        for i in range(langs):
            langs_str += "languages.language = ?"
            langs_list.append(langs[i])

            if i != len(topics) - 1:
                langs_str += " OR "


        limit_string = ""
        
        if args["amount"]:
            limit_string = f"LIMIT = ?"

        #SQL QUERYS
        result_list = None
        if args['topic']:
            books = args['books'].split(',')
            topics = args['topics'].split(',')

            #SQL Where Books
            book_str = ""
            book_list = []
            for i in range(books):
                book_str += "books.book = ?"
                book_list.append(books[i])

                if i != len(books) - 1:
                    book_str += " OR "
            
            #SQL WHERE Topics
            topic_str = ""
            topic_list = []
            for i in range(topics):
                topic_str += "or topics.topic = ?"
                topic_list.append(topics[i])

                if i != len(topics) - 1:
                    topic_str += " OR "

            result_list = db.query_dict(f"""
                                    SELECT vocabulary.word, vocabulary.translation 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN topics ON topics.id = vocabulary.topic
                                    WHERE ({book_str}) AND ({topic_str}) AND ({langs_str})
                                    ORDER BY random() {limit_string}
                                    """, tuple(book_list + topic_list + langs_list + ([args['amount']] if args["amount"] else [])))
        else:
            units = args['units'].split(',')  

            unit_str = ""
            unit_list = []
            for i in range(units):
                unit_str += "units.unit = ?"
                unit_list.append(units[i])

                if i != len(units) - 1:
                    unit_str += " OR "

            result_list = db.query_dict(f"""
                                    SELECT vocabulary.word, vocabulary.translation 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN units ON units.id = vocabulary.unit
                                    WHERE ({unit_str}) AND ({langs_str}) 
                                    ORDER BY random() LIMIT ?
                                    """, tuple(unit_list + langs_list + ([args['amount']] if args["amount"] else [])))
        return result_list, 200

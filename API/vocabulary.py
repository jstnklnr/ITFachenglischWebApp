from flask_restful import Resource
from flask_restful import reqparse
from flask import Flask, request
import random
import static

class Vocabulary(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("book", type = str)
        self.reqparse.add_argument("topic", type = str)
        self.reqparse.add_argument("unit", type = str)
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        db = static.database
        args = self.reqparse.parse_args()
        
        print(args["book"])

        #parameter missing
        if not args['book']:
            return {"Error": "Books is missing."}, 400
        if not args['lang']:
            return {"Error": "Language is missing."}, 400
        if ',' in args['book']:
            if args['unit']:
                return {"Error": "Can't use units for more then one book."}, 400
            if not args['topic']:
                return {"Error": "Topic is missing."}, 400
        else:
            if not args['unit']:
                return {"Error": "Unit is missing."}, 400
            if args['topic']:
                return {"Error": "Can't use topics for only one book."}, 400 
                
        #amount not acceptable
        if args["amount"] and args['amount'] < 1:
            return {"Error": "Amount is too low."}, 403


        #SQL WHERE Languages
        langs = args['lang'].split(',')
        langs_str = " OR ".join(["languages.language = ?"] * len(langs))

        limit_string = ""
        
        if args["amount"]:
            limit_string = f"LIMIT ?"

        
        #SQL Where Books
        books = args['book'].split(',')
        book_str = " OR ".join(["books.book = ?"] * len(books))

        #SQL QUERYS
        result_list = None
        if args['topic']:
            topics = args['topic'].split(',')
            
            #SQL WHERE Topics
            topic_str = " OR ".join(["topics.topic = ?"] * len(topics))

            result_list = db.query_dict(f"""
                                    SELECT vocabulary.word 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN topics ON topics.id = vocabulary.topic
                                    WHERE ({book_str}) AND ({topic_str}) AND ({langs_str})
                                    ORDER BY random() {limit_string}
                                    """, tuple(books + topics + langs + ([args['amount']] if args["amount"] else [])))
        else:
            units = args['unit'].split(',')
            unit_str = " OR ".join(["units.unit = ?"] * len(units))

            result_list = db.query_dict(f"""
                                    SELECT vocabulary.word 
                                    FROM vocabulary
                                    JOIN languages ON languages.id = vocabulary.language
                                    JOIN books ON books.id = vocabulary.book
                                    JOIN units ON units.id = vocabulary.unit
                                    WHERE ({book_str}) AND ({unit_str}) AND ({langs_str}) 
                                    ORDER BY random() {limit_string}
                                    """, tuple(books + units + langs + ([args['amount']] if args["amount"] else [])))
        return result_list, 200

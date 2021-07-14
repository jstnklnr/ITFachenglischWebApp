from flask import Flask
from flask import reqparse
from flask_restful import Resource

class Phrase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("lang", type = str)
        self.reqparse.add_argument("trans-lang", type = str)
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        args = self.reqparse.parse_args()

        #parameter missing
        if not args['amount']:
            return {"Error": "Amount is missing."}, 400
        if not args['lang']:
            return {"Error": "Language is missing."}, 400   
        if not args['trans-lang']:
            return {"Error": "Translation language is missing."}, 400  

        #amount not acceptable
        if args['amount'] > 100:
            return {"Error": "Amount is to high."}, 403
        if args['amount'] < 1:
            return {"Error": "Amount is to low."}, 403

        #SQL QUERYS
        resultList = db.query_dict(f"""
                                SELECT phrases.phrase,
                                FROM phrases
                                JOIN languages ON languages.id = vocabulary.language
                                WHERE languages.language = ?
                                ORDER BY random() LIMIT ?
                                """, tuple(args['lang'] + args['amount']))
        
        return resultList, 200

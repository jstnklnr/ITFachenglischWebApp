from flask import Flask
from flask import reqparse
from flask_restful import Resource

class Audio(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("amount", type = int)

    def get(self):
        args = self.reqparse.parse_args()

        #parameter missing
        if not args['amount']:
            return {"Error": "Amount is missing."}, 400

        #amount not acceptable
        if args['amount'] > 100:
            return {"Error": "Amount is to high."}, 403
        if args['amount'] < 1:
            return {"Error": "Amount is to low."}, 403

        resultList = db.query_dict(f"""
                                SELECT sentences.sentence, sentences.translation 
                                FROM sentences
                                ORDER BY random() LIMIT ?
                                """, tuple(args['amount']))
        
        return resultList, 200

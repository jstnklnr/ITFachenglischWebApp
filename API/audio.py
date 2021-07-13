from flask import Flask
from flask_restful import Resource

class Audio(Resource):
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

        #TODO
        if topic[0] == "all":
            words = db.select("vocabulary", ("languages"), where={"languages=": lang})
        else:
            words = db.select("vocabulary", )
                                
        return "hello world"
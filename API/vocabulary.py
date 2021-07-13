from flask_restful import Resource
from flask import request, jsonify, make_response
from main import db

import random

class Vocabulary(Resource):
    def get(self):
        topic = request.headers.get('topic')
        amount = request.headers.get('amount')
        lang = request.headers.get('lang')
        
        print(categories)###
        print(amount)###
        
        #header is missing
        if not topic:
            return {"Error": "Topic is missing."}, 400
        if not amount:
            return {"Error": "Amount is missing."}, 400
        if not lang1:
            return {"Error": "Fist language is missing."}, 400

        #amount not acceptable
        if amount > 100:
            return {"Error": "Amount is to high."}, 403
        if amount < 1:
            return {"Error": "Amount is to low."}, 403

        #TODO
        if topic[0] == "all":
            words = db.select("vocabulary", ("languages"), where={"languages=": lang})
        else:
            words = db.select("vocabulary", )
                                
        return "hello world"
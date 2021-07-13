from flask_restful import Resource
from flask import request, jsonify, make_response
from main import db

class Vocabulary(Resource):
    def get(self):
        categories = request.headers.get('categories')
        amount = request.headers.get('amount')
        
        print(categories)###
        print(amount)###
        
        #header is missing
        if not categories:
            return make_response({
                "Error": "Category is missing."
                }, 400)
                
        if not amount:
            return make_response({
                "Error": "Amount is missing."
                }, 400)
                
        #amount not acceptable
        if amount > 100:
            return make_response({
                "Error": "Amount is to high."
                }, 403)
        
        if amount < 1:
            return make_response({
                "Error": "Amount is to low."
                }, 403)
                
        
                
        words = db.select("vocabulary", )
                                
        return "hello world"
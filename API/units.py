
from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Units(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("book")

    def get(self):
        args = self.reqparser.parse_args()

        if not args["book"]:
            return {"Error": "Book is missing."}, 400
        
        db = static.database
        return db.query_dict("""
                            SELECT units.unit, t0.amount 
                            FROM units 
                            JOIN (SELECT units.id, COUNT(vocabulary.id) AS amount
                            FROM vocabulary
                            JOIN units ON units.id = vocabulary.unit
                            JOIN books ON books.id = vocabulary.book
                            WHERE books.book = ? GROUP BY units.id) AS t0
                            ON t0.id = units.id""", [args["book"]]), 200
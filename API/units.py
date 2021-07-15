
from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Units(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument("book")

    def get(self):
        if not args["book"]:
            return {"Error": "Book is missing."}, 400
        
        db = static.database
        return db.query_dict("SELECT units FROM units JOIN books ON book.id = units.book WHERE books.book = ?", args["book"]), 200
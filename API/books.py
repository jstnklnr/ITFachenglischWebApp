from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Books(Resource):
    def __init__(self):
        pass

    def get(self):
        db = static.database
        return db.query_dict("SELECT book FROM books"), 200
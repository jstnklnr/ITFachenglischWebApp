from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Topics(Resource):
    def __init__(self):
        pass

    def get(self):
        db = static.database
        return db.query_dict("SELECT topic FROM topics"), 200
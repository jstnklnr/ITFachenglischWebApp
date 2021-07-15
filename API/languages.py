
from flask import Flask
from flask_restful import reqparse
from flask_restful import Resource
import static

class Languages(Resource):
    def __init__(self):
        pass

    def get(self):
        db = static.database
        return db.query_dict("SELECT language FROM languages"), 200
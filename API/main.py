from flask import Flask
from flask_restful import Api
from vocabulary import Vocabulary
from database_interface import Database

app = Flask(__name__)
api = Api(app)

db = Database("dbstring")
api.add_resource(Vocabulary, '/Vocabulary')

app.run('0.0.0.0', port=5000)
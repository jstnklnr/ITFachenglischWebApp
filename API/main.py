import os

from flask import Flask
from flask_restful import Api

from vocabulary import Vocabulary
from audio import Audio
from translation import Translation
from phrase import Phrase

from database_interface import Database

app = Flask(__name__)
api = Api(app)

db = Database(f"{os.path.dirname(__file__)}\\..\\Database\\database.db")
api.add_resource(Vocabulary, '/Vocabulary')
api.add_resource(Audio, '/Audio')
api.add_resource(Translation, '/Translations')
api.add_resource(Phrase, '/Phrase')

app.run('0.0.0.0', port=5000)

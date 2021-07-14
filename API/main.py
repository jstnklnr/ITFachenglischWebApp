import os

from flask import Flask
from flask_restful import Api

from vocabulary import Vocabulary
from audio import Audio
from translation import Translation
from senctence import Sentence

from database_interface import Database

app = Flask(__name__)
api = Api(app)

db = Database(f"{os.path.dirname(__file__)}\\..\\Database\\database.db")
api.add_resource(Vocabulary, '/Vocabulary')
api.add_resource(Audio, '/Audio')
api.add_resource(Translation, '/Translations')
api.add_resource(Sentence, '/Sentence')

app.run('0.0.0.0', port=5000)

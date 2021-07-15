import os

from flask import Flask
from flask_restful import Api

from vocabulary import Vocabulary
from audio import Audio
from translation import Translation
from phrases import Phrases

from database_interface import Database
import static

app = Flask(__name__)
api = Api(app)

static.database = Database(f"{os.path.dirname(__file__)}\\..\\Database\\database.db")
api.add_resource(Vocabulary, '/vocabulary')
api.add_resource(Audio, '/audio')
api.add_resource(Translation, '/translation')
api.add_resource(Phrases, '/phrases')

app.run('0.0.0.0', ssl_context='adhoc', port=5000)

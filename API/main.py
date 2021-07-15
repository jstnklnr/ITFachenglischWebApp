import os

from flask import Flask
from flask_restful import Api

from vocabulary import Vocabulary
from audio import Audio
from translation import Translation
from phrases import Phrases
from books import Books
from units import Units
from topics import Topics

from database_interface import Database
import static

app = Flask(__name__)
api = Api(app)

with app.app_context():
    static.database = Database(f"{os.path.dirname(__file__)}/../Database/database.db")
    
api.add_resource(Vocabulary, '/vocabulary')
api.add_resource(Audio, '/audio')
api.add_resource(Translation, '/translation')
api.add_resource(Phrases, '/phrases')
api.add_resource(Books, '/books')
api.add_resource(Units, '/units')
api.add_resource(Topics, '/topics')

app.run('0.0.0.0', ssl_context='adhoc', port=5000)

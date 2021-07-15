from flask import Flask, blueprints

app = Flask(__name__)

from main_routes import main as main_blueprint
app.register_blueprint(main_blueprint)
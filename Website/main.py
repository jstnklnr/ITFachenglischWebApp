from flask import Flask
from flask import blueprints
from flask_session import Session

import cryptography

def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    from main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()
app.run('0.0.0.0', port=8080, ssl_context='adhoc', debug=True)
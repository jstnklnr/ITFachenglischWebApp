from flask import Flask, blueprints

def create_app():
    app = Flask(__name__)

    from main_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()
app.run('0.0.0.0', port=8080)
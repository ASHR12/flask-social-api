"""
Main Flask application entry point for the Social Media REST API.
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from database import init_db
from routes.routes import register_routes

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    from models.models import db
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    if not app.config.get('TESTING', False):
        init_db(app, db)
    register_routes(app, db, jwt)
    @app.route("/")
    def index():
        return {
            "message": "Welcome to the Social Media REST API.",
            "docs": "See /api or /api/auth for available endpoints."
        }, 200
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)

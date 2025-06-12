from flask import Flask
from .routes import main
from .cache import cache
from .db import db

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    
    db.init_app(app)
    cache.init_app(app)
    app.register_blueprint(main)
    
    return app

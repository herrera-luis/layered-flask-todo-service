from flask import Flask
from flask_migrate import Migrate, upgrade
from .config import Config
from .database.db import db


def init_migration():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        migrate = Migrate(app, db)
        # Apply migrations at startup
        upgrade()

    return app

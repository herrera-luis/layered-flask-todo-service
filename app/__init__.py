from flask import Flask
from flask_migrate import Migrate, upgrade
from .config import Config
from .infrastructure.database import db
from .presentation.routes import register_routes
import logging
from logging.handlers import RotatingFileHandler
import os
import json


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'asctime': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'pathname': record.pathname,
            'lineno': record.lineno
        }
        return json.dumps(log_data)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    log_level = app.config.get('LOG_LEVEL', logging.INFO)
    log_dir = app.config.get('LOG_DIR', 'logs')
    log_file = os.path.join(log_dir, 'todo_service.log')
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(JSONLogFormatter())
    file_handler.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
    logging.basicConfig(level=logging.INFO
                        )
    db.init_app(app)
    register_routes(app)

    return app

from flask import Flask
from .config import Config, JSONLogFormatter
from .database.db import db
from .api.v1.routes import blueprint_api_v1, blueprint_base
from logging.handlers import RotatingFileHandler
import logging
import os

logger = logging.getLogger(__name__)


def configure_logger(app):
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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    configure_logger(app)
    db.init_app(app)
    app.register_blueprint(blueprint_api_v1, url_prefix='/api/v1')
    app.register_blueprint(blueprint_base, url_prefix='')
    logger.info("App created successfully")
    return app

import os
import json
import logging


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'date': self.formatTime(record, self.datefmt),
            'levelname': record.levelname,
            'message': record.getMessage(),
            'pathname': record.pathname,
            'line': record.lineno
        }
        return json.dumps(log_data)


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL") or "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

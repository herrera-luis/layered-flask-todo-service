# config.py
import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL") or "postgresql://todo-user:todo-password@database/todo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

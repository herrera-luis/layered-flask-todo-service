from app.models.todo import Todo, db
from flask import abort
import logging

logger = logging.getLogger(__name__)


class TodoService:
    @staticmethod
    def create_todo(title, description=None, status="todo"):
        logger.info("Saving Todo to the database")
        todo = Todo(title=title, description=description, status=status)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def get_all_todos():
        logger.info("Getting all TODOs from the database")
        return Todo.query.all()

    @staticmethod
    def get_todo_by_id(todo_id):
        logger.info("Finding TODO by id: %d", todo_id)
        return get_or_404(Todo, todo_id)

    @staticmethod
    def update_todo(todo_id, title=None, description=None, status=None):
        logger.info("Updating TODO by id: %d", todo_id)
        todo = get_or_404(Todo, todo_id)
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if status is not None:
            todo.status = status
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo_id):
        logger.info("Deleting TODO by id: %d", todo_id)
        todo = get_or_404(Todo, todo_id)
        db.session.delete(todo)
        db.session.commit()
        return True


def get_or_404(model, primary_key):
    instance = db.session.get(model, primary_key)
    if instance is None:
        abort(404)
    return instance

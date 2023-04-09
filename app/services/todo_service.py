from app.models.todo import Todo, db
from flask import abort


class TodoService:
    @staticmethod
    def create_todo(title, description=None, status="todo"):
        todo = Todo(title=title, description=description, status=status)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def get_all_todos():
        return Todo.query.all()

    @staticmethod
    def get_todo_by_id(todo_id):
        return get_or_404(Todo, todo_id)

    @staticmethod
    def update_todo(todo_id, title=None, description=None, status=None):
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
        todo = get_or_404(Todo, todo_id)
        db.session.delete(todo)
        db.session.commit()
        return True


def get_or_404(model, primary_key):
    instance = db.session.get(model, primary_key)
    if instance is None:
        abort(404)
    return instance

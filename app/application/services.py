from app.domain.models import Todo, db


class TodoService:
    @staticmethod
    def create_todo(title, description=None):
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def get_all_todos():
        return Todo.query.all()

    @staticmethod
    def get_todo_by_id(todo_id):
        return Todo.query.get_or_404(todo_id)

    @staticmethod
    def update_todo(todo, title=None, description=None, status=None):
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if status is not None:
            todo.status = status
        db.session.commit()
        return todo

    @staticmethod
    def delete_todo(todo):
        db.session.delete(todo)
        db.session.commit()

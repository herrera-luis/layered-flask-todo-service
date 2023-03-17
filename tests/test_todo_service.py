import unittest
from app.application.services import TodoService
from app.domain.models import Todo
from app.infrastructure.database import db
from app.config import Config
from flask import Flask
from werkzeug.exceptions import NotFound


class TestTodoService(unittest.TestCase):

    def setUp(self):
        # Create an in-memory SQLite database for testing purposes
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_todo(self):
        title = "Test todo"
        description = "Test todo description"
        todo = TodoService.create_todo(
            title=title, description=description)
        self.assertIsInstance(todo, Todo)
        self.assertEqual(todo.title, title)
        self.assertEqual(todo.description, description)

    def test_get_all_todos(self):
        todos = TodoService.get_all_todos()
        self.assertIsInstance(todos, list)

    def test_update_todo(self):
        # Create a new todo item
        title = "Test todo"
        description = "Test todo description"
        todo = TodoService.create_todo(title=title, description=description)

        # Update the todo item
        new_title = "Updated test todo"
        new_description = "Updated test todo description"
        new_status = "done"

        updated_todo = TodoService.update_todo(todo.id,
                                               title=new_title,
                                               description=new_description,
                                               status=new_status)
        self.assertIsInstance(updated_todo, Todo)
        self.assertEqual(updated_todo.title, new_title)
        self.assertEqual(updated_todo.description, new_description)
        self.assertEqual(updated_todo.status, new_status)

    def test_delete_todo(self):
        # Create a new todo item
        title = "Test todo"
        description = "Test todo description"
        todo = TodoService.create_todo(title=title, description=description)

        # Delete the todo item
        result = TodoService.delete_todo(todo.id)
        self.assertTrue(result)

        # Try to get the deleted todo item
        with self.assertRaises(NotFound):
            TodoService.get_todo_by_id(todo.id)


if __name__ == '__main__':
    unittest.main()

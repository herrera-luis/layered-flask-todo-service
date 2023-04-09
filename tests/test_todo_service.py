import unittest
from unittest.mock import patch
from app.services.todo_service import TodoService
from app.models.todo import Todo
from app.database.db import db
from app.config import Config
from flask import Flask
from werkzeug.exceptions import NotFound
import logging


class TestTodoService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create an in-memory SQLite database for testing purposes
        cls.app = Flask(__name__)
        cls.app.config.from_object(Config)
        db.init_app(cls.app)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    def setUp(self):
        self.log_patcher_service = patch(
            "app.services.todo_service.logger")
        self.mock_log = self.log_patcher_service.start()
        logging.disable(logging.INFO)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def tearDown(self):
        self.log_patcher_service.stop()
        logging.disable(logging.NOTSET)

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
        todo = TodoService.create_todo(
            title="Test todo", description="Test todo description")

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
        todo = TodoService.create_todo(
            title="Test todo", description="Test todo description")

        # Delete the todo item
        result = TodoService.delete_todo(todo.id)
        self.assertTrue(result)

        # Try to get the deleted todo item
        with self.assertRaises(NotFound):
            TodoService.get_todo_by_id(todo.id)


if __name__ == '__main__':
    unittest.main()

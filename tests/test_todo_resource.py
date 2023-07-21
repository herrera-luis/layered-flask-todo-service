import json
import unittest
import logging
from unittest.mock import patch
from app import create_app, db
from app.models.todo import Todo


class TodoResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    def setUp(self):
        self.log_patcher_resources = patch(
            "app.api.v1.resources.todo.logger")
        self.mock_log = self.log_patcher_resources.start()
        logging.disable(logging.INFO)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def tearDown(self):
        self.log_patcher_resources.stop()
        logging.disable(logging.NOTSET)

    def create_todo(self, title="Test todo", description="Test todo description"):
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        return todo

    def test_create_todo(self):
        response = self.client.post(
            "/api/v1/todos",
            json={"title": "Test Todo", "description": "Test todo description"})
        self.assertEqual(response.status_code, 201)

    def test_get_todos(self):
        response = self.client.get("/api/v1/todos")
        self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        todo = self.create_todo()

        response = self.client.put(
            f"/api/v1/todos/{todo.id}",
            data=json.dumps({"title": "Updated test todo",
                             "description": "Updated test todo description"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        todo = self.create_todo()
        response = self.client.delete(f"/api/v1/todos/{todo.id}")
        self.assertEqual(response.status_code, 204)

    def test_get_todo(self):
        todo = self.create_todo()

        response = self.client.get(f"/api/v1/todos/{todo.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_input(self):
        response = self.client.post(
            "/api/v1/todos",
            json={
                "description": "Test todo description",
                "done": False,
            },
        )
        self.assertEqual(response.status_code, 500)

    def test_update_nonexistent_todo(self):
        response = self.client.put(
            "/api/v1/todos/99999999",
            json={
                "title": "Updated test todo",
                "description": "Updated test todo description",
                "done": True,
            },
        )
        self.assertEqual(response.status_code, 500)

    def test_delete_nonexistent_todo(self):
        response = self.client.delete(
            "/api/v1/todos/99999999",
            json={
                "title": "Delete test todo",
                "description": "Delete test todo description",
                "done": True,
            },
        )
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()

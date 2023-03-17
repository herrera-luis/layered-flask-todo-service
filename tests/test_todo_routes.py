import json
import unittest
from app import create_app, db
from app.domain.models import Todo


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_todo(self):
        response = self.client.post(
            "/todos",
            data=json.dumps(
                {"title": "Test todo", "description": "Test todo description"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_get_todos(self):
        response = self.client.get("/todos")
        self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        # Create a new todo item
        todo = Todo(title="Test todo", description="Test todo description")
        db.session.add(todo)
        db.session.commit()

        # Send a PUT request to update the todo item
        response = self.client.put(
            f"/todos/{todo.id}",
            data=json.dumps({"title": "Updated test todo",
                            "description": "Updated test todo description"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        # Create a new todo item
        todo = Todo(title="Test todo", description="Test todo description")
        db.session.add(todo)
        db.session.commit()

        # Send a DELETE request to delete the todo item
        response = self.client.delete(f"/todos/{todo.id}")

        self.assertEqual(response.status_code, 204)

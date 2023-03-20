from flask import request, jsonify
from app.application.services import TodoService


def register_routes(app):
    @app.route('/todos', methods=['POST'])
    def create_todo():
        data = request.get_json()
        todo = TodoService.create_todo(
            title=data['title'], description=data.get('description', None), status=data.get('status', 'todo'))
        app.logger.info(f"Todo created: {todo.serialize()}")
        return jsonify(todo.serialize()), 201

    @app.route('/todos', methods=['GET'])
    def list_todos():
        todos = TodoService.get_all_todos()
        app.logger.info(f"Todo listed")
        return jsonify([t.serialize() for t in todos])

    @app.route('/todos/<int:todo_id>', methods=['GET'])
    def get_todo(todo_id):
        todo = TodoService.get_todo_by_id(todo_id)
        app.logger.info(f"Todo get")
        return jsonify(todo.serialize())

    @app.route('/todos/<int:todo_id>', methods=['PUT'])
    def update_todo(todo_id):
        data = request.get_json()
        todo = TodoService.get_todo_by_id(todo_id)
        updated_todo = TodoService.update_todo(todo_id,
                                               title=data.get('title', None),
                                               description=data.get(
                                                   'description', None),
                                               status=data.get('status', None))
        app.logger.info(f"Todo updated")
        return jsonify(updated_todo.serialize())

    @app.route('/todos/<int:todo_id>', methods=['DELETE'])
    def delete_todo(todo_id):
        todo = TodoService.get_todo_by_id(todo_id)
        TodoService.delete_todo(todo_id)
        app.logger.info(f"Todo deleted: {todo.serialize()}")
        return jsonify({"message": "Todo deleted"}), 204

from flask_restx import Namespace, Resource, fields
from app.services.todo_service import TodoService
import logging

logger = logging.getLogger(__name__)

api = Namespace('todos', description='TODO operations')

todo_model = api.model('TODO', {
    'id': fields.Integer(readonly=True, description='The unique identifier of the todo'),
    'title': fields.String(required=True, description='The title of the todo'),
    'description': fields.String(description='The description of the todo'),
    'status': fields.String(description='The status of the todo'),
    "created_at": fields.DateTime(description='The date when the todo was created')
})

todo_parser = api.parser()
todo_parser.add_argument(
    'title', type=str, required=True, help='Title is required')
todo_parser.add_argument('description', type=str, default='')
todo_parser.add_argument('status', type=str, default='todo')


@api.route('/<int:todo_id>')
class TodoResource(Resource):
    @api.doc('get_todo')
    @api.marshal_with(todo_model)
    def get(self, todo_id):
        try:
            logger.info("GET request for Todo with id: %d", todo_id)
            todo = TodoService.get_todo_by_id(todo_id)
            if todo:
                return todo, 200
        except Exception as e:
            logger.error(
                "Error while processing GET request TODO with id: %d \n Cause: %s" % (todo_id, str(e)))
        return {"message": "An error occurred while fetching the TODO"}, 404

    @api.doc('update_todo')
    @api.expect(todo_parser)
    @api.marshal_with(todo_model)
    def put(self, todo_id):
        try:
            logger.info("PUT request for TODO with id: %d", todo_id)
            args = todo_parser.parse_args()
            todo_updated = TodoService.update_todo(todo_id,
                                                   title=args['title'],
                                                   description=args['description'],
                                                   status=args['status'])
            if todo_updated:
                return todo_updated, 200
        except Exception as e:
            logger.error(
                "Error while processing PUT request TODO with id: %d \n Cause: %s" % (todo_id, str(e)))
        return {"message": "An error occurred while updating the TODO"}, 500

    @api.doc('delete_todo')
    @api.response(204, 'Todo deleted')
    def delete(self, todo_id):
        try:
            logger.info("DELETE request for TODO with id: %d", todo_id)
            if TodoService.delete_todo(todo_id):
                return 'Todo deleted', 204
        except Exception as e:
            logger.error(
                "Error while processing DELETE request TODO with id: %d \n Cause: %s" % (todo_id, str(e)))
        return {"message": "An error occurred while deleting the TODO"}, 500


@ api.route('/')
class TodoListResource(Resource):
    @ api.doc('list_todos')
    @ api.marshal_list_with(todo_model)
    def get(self):
        logger.info(f"GET request for all TODOs")
        todos = TodoService.get_all_todos()
        return todos, 200

    @ api.doc('create_todo')
    @ api.expect(todo_parser)
    @ api.marshal_with(todo_model, code=201)
    def post(self):
        try:
            logger.info(f"POST request to create a TODO")
            args = todo_parser.parse_args()
            todo = TodoService.create_todo(
                title=args['title'], description=args['description'], status=args['status'])
            return todo, 201
        except Exception as e:
            logger.error(
                "Error while creating POST request TODO \n Cause: %s", str(e))
        return {"message": "An error occurred while creating the TODO"}, 500

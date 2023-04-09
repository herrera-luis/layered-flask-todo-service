from flask_restx import Namespace, Resource, fields
from app.services.todo_service import TodoService

api = Namespace('todos', description='Todo operations')

todo_model = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The unique identifier of the todo'),
    'title': fields.String(required=True, description='The title of the todo'),
    'description': fields.String(description='The description of the todo'),
    'status': fields.String(description='The status of the todo'),
})

todo_parser = api.parser()
todo_parser.add_argument(
    'title', type=str, required=True, help='Title is required')
todo_parser.add_argument('description', type=str, default='')
todo_parser.add_argument('status', type=str, default='todo')


@api.route('/<int:todo_id>')
@api.response(404, 'Todo not found')
class TodoResource(Resource):
    @api.doc('get_todo')
    @api.marshal_with(todo_model)
    def get(self, todo_id):
        todo = TodoService.get_todo_by_id(todo_id)
        if todo:
            return todo, 200
        api.abort(404)

    @api.doc('update_todo')
    @api.expect(todo_parser)
    @api.marshal_with(todo_model)
    def put(self, todo_id):
        args = todo_parser.parse_args()
        todo_updated = TodoService.update_todo(todo_id,
                                               title=args['title'],
                                               description=args['description'],
                                               status=args['status'])
        if todo_updated:
            return todo_updated, 200
        api.abort(404)

    @api.doc('delete_todo')
    @api.response(204, 'Todo deleted')
    def delete(self, todo_id):
        if TodoService.delete_todo(todo_id):
            return '', 204
        api.abort(404)


@api.route('/')
class TodoListResource(Resource):
    @api.doc('list_todos')
    @api.marshal_list_with(todo_model)
    def get(self):
        todos = TodoService.get_all_todos()
        return todos, 200

    @api.doc('create_todo')
    @api.expect(todo_parser)
    @api.marshal_with(todo_model, code=201)
    def post(self):
        args = todo_parser.parse_args()
        todo = TodoService.create_todo(
            title=args['title'], description=args['description'], status=args['status'])
        return todo, 201

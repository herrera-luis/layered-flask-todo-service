from flask import Blueprint
from flask_restx import Api
from flask import jsonify
from app.api.v1.resources.todo import api as todo_ns

blueprint_api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
blueprint_base = Blueprint('base', __name__, url_prefix='')

api = Api(blueprint_api_v1,
          title='TODO API',
          version='1.0',
          description='A simple TODO API',
          doc='/doc/')

api.add_namespace(todo_ns)


@blueprint_base.route('/', methods=['GET'])
def get():
    return 'TODO API'


@blueprint_base.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify(status='healthy', message='API is running')

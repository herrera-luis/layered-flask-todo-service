from flask import Blueprint
import socket
import platform
import datetime
from flask_restx import Api
from flask import jsonify
from app.api.v1.resources.todo import api as todo_ns

blueprint_api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
blueprint_base = Blueprint('base', __name__, url_prefix='')

api = Api(blueprint_api_v1,
          title='TODOs API',
          version='1.0',
          description='A simple TODOs API',
          doc='/doc/')

api.add_namespace(todo_ns)


@blueprint_base.route('/', methods=['GET'])
def get():
    os_info = platform.system()  # Get OS info
    os_version = platform.release()  # Get OS version
    current_time = datetime.datetime.now().isoformat()  # Get current time
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return jsonify({'OS': os_info, "OS Version": os_version, 'Hostname': host_name, 'IP': host_ip, 'Time': current_time})


@blueprint_base.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify(status='healthy', message='API is running')

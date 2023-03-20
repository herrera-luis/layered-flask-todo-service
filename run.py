from app import create_app
from flask_cors import CORS
import os

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})
if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv(
        'PORT'))

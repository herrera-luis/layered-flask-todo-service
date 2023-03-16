from app import create_app
import os
import logging

app = create_app()
logging.getLogger().setLevel(logging.INFO)
if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv(
        'PORT'))

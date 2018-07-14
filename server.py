import os

from flask import Flask, request
from flask_cors import CORS

from nobugs import nobugs

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
if os.environ['ENV_TYPE'] == 'Dev':
    app.config['DEBUG'] = True


@app.route('/api/email', methods=['POST'])
def email():
    # Post email address when client sends the jsonified email address
    if request.method == 'POST':
        return nobugs.create_email()

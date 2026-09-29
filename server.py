import os

from flask import Flask
from flask_cors import CORS

from nobugs import nobugs

app = Flask(__name__)
# Only the NoBugs! site may call the API from a browser
cors = CORS(app, resources={r"/api/*": {"origins": [
    'https://nobugsphilly.com', 'https://www.nobugsphilly.com']}})
if os.environ.get('ENV_TYPE') == 'Dev':
    app.config['DEBUG'] = True


@app.route('/api/email', methods=['POST'])
def email():
    # Post email address when client sends the jsonified email address
    return nobugs.create_email()

import json
import unittest

from server import app
from unittest.mock import patch


# Test /api/email endpoint [POST]
class TestEmail(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('google.auth.app_engine.Credentials')
    @patch('googleapiclient.http.HttpRequest.execute',
        return_value={'values': []})
    def test_email_post_data(self, Credentials, request):
        # Arrange
        data = {
            'email': 'test@test.com'
        }

        # Act
        post_response = self.client.post(
            '/api/email',
            data=json.dumps(data),
            content_type='application/json'
            )
        email = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(email, 'test@test.com')

    def test_email_post_data_error(self):
        # Act
        post_response = self.client.post(
            '/api/email'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(
            error, 'Request must contain email address')

    def test_email_post_email_error(self):
        # Arrange
        data = {
            'email': ['test@test.com']
        }

        # Act
        post_response = self.client.post(
            '/api/email',
            data=json.dumps(data),
            content_type='application/json'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(error, 'Email address must be a string')

    def test_email_post_invalid_error(self):
        # Arrange
        data = {
            'email': 'email'
        }

        # Act
        post_response = self.client.post(
            '/api/email',
            data=json.dumps(data),
            content_type='application/json'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(error, 'Invalid email address')

    @patch('google.auth.app_engine.Credentials')
    @patch('googleapiclient.http.HttpRequest.execute',
        return_value={'values': [['test@test.com']]})
    def test_email_post_email_exists(self, Credentials, request):
        # Arrange
        data = {
            'email': 'test@test.com'
        }

        # Act
        post_response = self.client.post(
            '/api/email',
            data=json.dumps(data),
            content_type='application/json'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 409)
        self.assertEqual(error, 'Email address already on mailing list')

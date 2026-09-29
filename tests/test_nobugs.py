import json
import unittest
from unittest.mock import MagicMock, patch

from nobugs import nobugs
from server import app


# Test /api/email endpoint [POST]
class TestEmail(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        nobugs._attempts.clear()

        # Stub the Sheets service; `sheet` holds the rows the get call returns
        self.sheet = {'values': []}
        patchers = [
            patch('google.auth.default', return_value=(MagicMock(), None)),
            patch.object(nobugs.discovery, 'build'),
            ]
        mocks = [p.start() for p in patchers]
        for p in patchers:
            self.addCleanup(p.stop)
        self.values = mocks[1].return_value.spreadsheets.return_value.values
        self.values.return_value.get.return_value.execute.side_effect = (
            lambda: self.sheet)

    def post(self, email, **kwargs):
        return self.client.post(
            '/api/email',
            data=json.dumps({'email': email}),
            content_type='application/json',
            **kwargs
            )

    def appended(self):
        return self.values.return_value.append.call_args

    def test_email_post_data(self):
        post_response = self.post('test@test.com')

        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.get_data(as_text=True), 'test@test.com')
        self.assertEqual(self.appended().kwargs['body'],
            {'values': [['test@test.com']]})

    def test_email_post_data_error(self):
        post_response = self.client.post('/api/email')

        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(post_response.get_data(as_text=True),
            'Request must contain email address')

    def test_email_post_email_error(self):
        post_response = self.post(['test@test.com'])

        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(post_response.get_data(as_text=True),
            'Email address must be a string')

    def test_email_post_invalid_error(self):
        post_response = self.post('email')

        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(post_response.get_data(as_text=True),
            'Invalid email address')
        self.assertEqual(post_response.mimetype, 'text/plain')

    def test_email_post_email_exists(self):
        self.sheet = {'values': [['test@test.com']]}

        post_response = self.post('test@test.com')

        self.assertEqual(post_response.status_code, 409)
        self.assertEqual(post_response.get_data(as_text=True),
            'Email address already on mailing list')
        self.assertIsNone(self.appended())

    def test_email_empty_sheet(self):
        # A sheet with no rows omits `values` entirely
        self.sheet = {}

        self.assertEqual(self.post('test@test.com').status_code, 201)

    def test_email_append_is_raw(self):
        # A formula-shaped local part is a valid address, so it must be
        # stored as text rather than evaluated by the spreadsheet
        post_response = self.post('=1+1@test.com')

        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(self.appended().kwargs['valueInputOption'], 'RAW')
        self.assertEqual(self.appended().kwargs['body'],
            {'values': [['=1+1@test.com']]})

    def test_email_too_long(self):
        self.assertEqual(self.post('a' * 250 + '@test.com').status_code, 400)
        self.assertIsNone(self.appended())

    def test_email_rate_limited(self):
        self.assertEqual(nobugs.RATE_LIMIT, 5)

        statuses = [self.post('test%d@test.com' % i).status_code
            for i in range(6)]

        self.assertEqual(statuses, [201] * 5 + [429])
        self.assertEqual(self.values.return_value.append.call_count, 5)

    def test_cors_allows_only_the_site(self):
        allowed = self.post('email', headers={
            'Origin': 'https://nobugsphilly.com'})
        other = self.post('email', headers={'Origin': 'https://evil.test'})

        self.assertEqual(allowed.headers.get('Access-Control-Allow-Origin'),
            'https://nobugsphilly.com')
        self.assertIsNone(other.headers.get('Access-Control-Allow-Origin'))

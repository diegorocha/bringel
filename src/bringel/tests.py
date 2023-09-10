import logging

import jwt
from django.conf import settings
from django.test import TestCase

from bringel.jwt import jwt_token_generator
from bringel.logs import JSONFormatter


class JWTTestCase(TestCase):
    def test_jwt_token_generator_has_jti_and_exp(self):
        secret = settings.SECRET_KEY
        token = jwt_token_generator()

        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertIn('jti', decoded)
        self.assertIn('exp', decoded)


class JSONFormatterTestCase(TestCase):
    def test_json_record_contains_level_pathname_lineno(self):
        with self.assertLogs('foo', level='INFO') as cm:
            logging.getLogger('foo').info('first message')
            message = cm.output[0]
            record = cm.records[0]
        extra = {}
        self.assertNotIn('level', extra)
        self.assertNotIn('pathname', extra)
        self.assertNotIn('lineno', extra)
        json_record = JSONFormatter().json_record(message, extra, record)
        self.assertIn('level', json_record)
        self.assertIn('pathname', json_record)
        self.assertIn('lineno', json_record)
        self.assertIn('level', extra)
        self.assertIn('pathname', extra)
        self.assertIn('lineno', extra)

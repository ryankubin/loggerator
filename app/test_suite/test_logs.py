import unittest
from unittest.mock import patch
from mongomock import MongoClient
from dateutil import parser
from app import create_app
from log_stream import process_log
import db as db

raw_log = b'249.87.118.62 - ryantest [21/Jul/2000 11:47:23 +0000] "GET /photos/121 HTTP/1.0" 500 441\n'

test_log = {
        "ip_address": "249.87.118.62",
        "user": "ryantest",
        "datetime": parser.parse("21/Jul/2000 11:47:23 +0000").isoformat(),
        "method": "GET",
        "requested_resource": "/photos/121",
        "protocol": "HTTP/1.0",
        "code": 500,
        "bytes_sent": 441,
        "raw": '249.87.118.62 - ryantest [21/Jul/2000 11:47:23 +0000] "GET /photos/121 HTTP/1.0" 500 441\n',
    }

if 'unittest.util' in __import__('sys').modules:
    # Show full diff in self.assertEqual.
    __import__('sys').modules['unittest.util']._MAX_LENGTH = 999999999

class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()

class TestLogs(unittest.TestCase):
    def test_create_log(self):
        with patch.object(db, "mongo", PyMongoMock()):
            app = create_app().test_client()
            log = process_log(raw_log.decode("utf-8"))
            self.assertEqual(log, test_log)

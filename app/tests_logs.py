import unittest

from app import create_app
from log_stream import process_log


class TestLogs(unittest.TestCase):
    def test_ingest_log_bad_port(self):
        data = {"port": 800000}
        app = create_app().test_client()
        response = app.post("/logs", json=data)
        self.assertEqual(response.status_code, 400)

    def test_ingest_log_wrong_host(self):
        data = {"host": "http://172.17.0.0"}
        app = create_app().test_client()
        response = app.post("/logs", json=data)
        self.assertEqual(response.status_code, 502)

    def test_get_log_bad_params(self):
        app = create_app().test_client()
        response = app.get("/logs?limit=twofeet")
        self.assertEqual(response.status_code, 400)

        response = app.get("/logs?page=third")
        self.assertEqual(response.status_code, 400)

    def test_process_line(self):
        line = '249.87.118.62 - marilyntorres [30/Jul/2000 07:15:18 +0000] "PUT /likes/66 HTTP/1.0" 403 320\n'
        processed_line = {
            "ip_address": "249.87.118.62",
            "user": "marilyntorres",
            "datetime": "2000-07-30T07:15:18+00:00",
            "method": "PUT",
            "requested_resource": "/likes/66",
            "protocol": 'HTTP/1.0"',
            "code": "403",
            "bytes_sent": "320",
            "raw": '249.87.118.62 - marilyntorres [30/Jul/2000 07:15:18 +0000] "PUT /likes/66 HTTP/1.0" 403 320',
        }
        p_line = process_log(line)
        self.assertEqual(p_line, processed_line)

    def test_bad_process_line(self):
        line = '249.87.118.62 - [30/Jul/2000 07:15:18 +0000] "PUT /likes/66 HTTP/1.0" 403 320\n'
        p_line = process_log(line)
        self.assertEqual(p_line, {})

    """
    I would want to either create a separate test db to manage pieces touching that,
    or mock a db instance using MongoMock.
    These would include tests on ingestion, tests on get, and tests on delete (basic CRUD, nothing revolutionary here)
    """

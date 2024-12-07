import unittest
import json
from api.app import app

class TestAPU(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_rooms(self):
        response = self.app.get('/api/rooms')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
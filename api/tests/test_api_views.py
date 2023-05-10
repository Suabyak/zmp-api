from django.test import TestCase, Client

class TestApi(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        
    def test_get_token(self):
        response = self.client.get("/api/token/")
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post("/api/token/")
        self.assertNotEqual(response.status_code, 200)
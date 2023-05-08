from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class TestModels(TestCase):
    def setUp(self):
        user = User.objects.create_user("Test User", "test@email.com", "test")
    
    def test_user_registration(self):
        simeno = authenticate(username="Test User", password="test")
        self.assertEqual(simeno.username, "Test User")
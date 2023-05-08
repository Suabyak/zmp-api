from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class TestModels(TestCase):
    def test_user_registration(self):
        User.objects.create_user("Test User", "test@email.com", "test")
        simeno = authenticate(username="Test User", password="test")
        self.assertEqual(simeno.username, "Test User")
    
    def test_post_creation(self):
        pass
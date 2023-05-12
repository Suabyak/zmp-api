from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Post
from api.views.users import get_token_for_user

class TestViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post("/api/users/sign-up/", 
                         {"username" : "Suabyak", 
                          "email" : "suaby@email.com",
                          "password" : "suabo",
                          "password_confirm" : "suabo"})
        self.user = User.objects.first()
        self.token = get_token_for_user(self.user)
    
    def test_create_post(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum"}, 
                                    **{"token" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum"},
                                    **{"token" : "Wrong token"})
        self.assertEqual(response.data["success"], False)
    
    def test_get_user_posts(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum"}, 
                                    **{"token" : self.token})
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorua Merleu"}, 
                                    **{"token" : self.token})
        
        response = self.client.get(f"/api/posts/get/{self.user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["posts"]), 2)
        self.assertEqual(response.data["posts"][1]["body"], "Lorua Merleu")

        response = self.client.get(f"/api/posts/get/1827368712638612836812686/")
        self.assertEqual(response.data["success"], False)
        
        
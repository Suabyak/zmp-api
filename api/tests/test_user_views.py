from django.test import TestCase, Client
from django.contrib.auth.models import User
from api.models import Comment
from api.utils.jwt_token import get_token_for_user
from api.utils.models import serialize_model_list

class TestViews(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        
        self.client.post("/api/users/sign-up/", 
                         {"username" : "Suabyak", 
                          "email" : "suaby@email.com",
                          "password" : "suabo",
                          "password_confirm" : "suabo"})
        self.user = User.objects.first()
        self.token = get_token_for_user(self.user)
    
    def test_sign_up_user(self):
        response = self.client.post("/api/users/sign-up/", 
                                    {"username" : "TestUser", 
                                     "email" : "test@email.com",
                                     "password" : "test",
                                     "password_confirm" : "test"})
        self.assertEqual(response.data["success"], True)
        
        response = self.client.post("/api/users/sign-up/", 
                                    {"username" : "TestUser", 
                                     "email" : "test@email.com",
                                     "password" : "test",
                                     "password_confirm" : "test2"})
        self.assertEqual(response.data["success"], False)
        
        response = self.client.get("/api/users/sign-up/", 
                                    {"username" : "TestUser", 
                                     "email" : "test@email.com",
                                     "password" : "test",
                                     "password_confirm" : "test2"})
        self.assertEqual(response.status_code, 405)
    
    def test_sign_in_user(self):
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suabyak", 
                                     "password" : "suabo"})
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Successfully logged in")
        
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suaby", 
                                     "password" : "suabo"})
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["message"], "Invalid username or password")
        
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suabyak", 
                                     "password" : "suaboooo"}) 
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["message"], "Invalid username or password")
        
        response = self.client.get("/api/users/sign-in/")
        self.assertEqual(response.status_code, 405)
    
    def test_get_user_data(self):
        response = self.client.get("/api/users/get-user-data/", 
                                    {"id" : self.user.id})
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["success"], True)
        
        
        response = self.client.get("/api/users/get-user-data/", 
                                    {"id" : -3})
        self.assertEqual(response.data["success"], False)
        
        
        response = self.client.post("/api/users/get-user-data/", 
                                    {"id" : self.user.id})
        self.assertEqual(response.status_code, 405)
    
    def test_get_users_by_search(self):
        response = self.client.get("/api/users/get-users-by-search/", 
                                    {"search" : "abya"})
        self.assertEqual(response.data["users"][0]["username"], self.user.username)
        
        response = self.client.get("/api/users/get-users-by-search/", 
                                    {"search" : "Suabyak"})
        self.assertEqual(response.data["users"][0]["username"], self.user.username)
        
        response = self.client.get("/api/users/get-users-by-search/", 
                                    {"search" : "Suabyako"})
        self.assertEqual(response.data["users"], [])
        
        response = self.client.post("/api/users/get-users-by-search/", 
                                    {"search" : "Suabyako"})
        self.assertEqual(response.status_code, 405)
        
    def test_get_user(self):
        response = self.client.get("/api/user/", **{"token" : self.token})
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["user_id"], self.user.id)
        
        response = self.client.get("/api/user/", **{"token" : "Wrong token"})
        self.assertEqual(response.data["message"], "Wrong token")
        
        response = self.client.post("/api/user/", **{"token" : "Wrong token"})
        self.assertEqual(response.status_code, 405)
    
    def test_get_comments_by_id(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum"}, 
                                    **{"token" : self.token})
        id = response.data['id']
        
        response = self.client.post(f"/api/post/{id}/comment/", 
                                    {"body": "Fajny post :]"},
                                    **{"token" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/user/{self.user.id}/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["comments"]), 1)
        
        response = self.client.post(f"/api/post/{id}/comment/", 
                                    {"body": "SUPER Fajny post :]"},
                                    **{"token" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/user/{self.user.id}/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["comments"]), 2)
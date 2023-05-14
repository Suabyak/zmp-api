from django.test import TestCase, Client
from django.contrib.auth.models import User
from api.utils.jwt_token import get_token_for_user

class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        
        self.client.post("/api/users/sign-up/", 
                         {"username" : "Suabyak", 
                          "email" : "suaby@email.com",
                          "password" : "suabo",
                          "password_confirm" : "suabo"})
        self.user = User.objects.first()
        self.token = f"Bearer {get_token_for_user(self.user)}"
    
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
        self.assertEqual(response.status_code, 530)
        
        response = self.client.get("/api/users/sign-up/", 
                                    {"username" : "TestUser", 
                                     "email" : "test@email.com",
                                     "password" : "test",
                                     "password_confirm" : "test2"})
        self.assertEqual(response.status_code, 405)
        
        response = self.client.post("/api/users/sign-up/", 
                                    {"password" : "test",
                                     "password_confirm" : "test2"})
        self.assertEqual(response.status_code, 530)
    
    def test_sign_in_user(self):
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suabyak", 
                                     "password" : "suabo"})
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Successfully logged in")
        
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suaby", 
                                     "password" : "suabo"})
        self.assertEqual(response.status_code, 530)
        self.assertEqual(response.status_code, 530)
        self.assertEqual(response.data["message"], "Invalid username or password")
        
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suabyak", 
                                     "password" : "suaboooo"}) 
        self.assertEqual(response.status_code, 530)
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
        self.assertEqual(response.status_code, 530)
        
        
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
        response = self.client.get("/api/user/", **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["user_id"], self.user.id)
        
        response = self.client.get("/api/user/", **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.data["message"], "Wrong token")
        
        response = self.client.post("/api/user/", **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 405)
    
    def test_get_comments_by_id(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id = response.data['id']
        
        response = self.client.post(f"/api/post/{id}/comment/", 
                                    {"body": "Fajny post :]"},
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/user/{self.user.id}/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["comments"]), 1)
        
        response = self.client.post(f"/api/post/{id}/comment/", 
                                    {"body": "SUPER Fajny post :]"},
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/user/{self.user.id}/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["comments"]), 2)
    
    def test_add_observation(self):
        response = self.client.post(f"/api/user/observe/", 
                            {"id": self.user.id},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/user/observe/", 
                            {"id": self.user.id},
                            **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 405)
        
        response = self.client.post(f"/api/user/observe/", 
                            {},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 530)

    def test_set_profile(self):
        response = self.client.post(f"/api/user/profile/set/", 
                            {"file": "zdjencie"},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/user/profile/set/", 
                            {"file": "zdjencie"},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 405)
        
        response = self.client.post(f"/api/user/profile/set/", 
                            {},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 530)
        
        response = self.client.post(f"/api/user/profile/set/", 
                            {"file": "zdjencie"},
                            **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 531)
    
    def test_get_observed(self):
        response = self.client.post(f"/api/user/observe/", 
                            {"id": self.user.id},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get("/api/user/observed/",
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        
        response = self.client.post(f"/api/user/observe/", 
                            {"id": self.user.id},
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get("/api/user/observed/",
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
        
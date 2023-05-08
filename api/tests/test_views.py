from django.test import TestCase, Client
from django.contrib.auth.models import User
from ast import literal_eval

def dict_from_json_response(response):
    return literal_eval(response.content.decode(response.charset).replace("true", "True").replace("false", "False"))

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post("/api/users/sign-up/", 
                         {"username" : "Suabyak", 
                          "email" : "suaby@email.com",
                          "password" : "suabo",
                          "password_confirm" : "suabo"})
    
    def test_sign_up_user(self):
        response = self.client.post("/api/users/sign-up/", 
                                    {"username" : "TestUser", 
                                     "email" : "test@email.com",
                                     "password" : "test",
                                     "password_confirm" : "test"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], True)
        
        response = self.client.post("/api/users/sign-up/", 
                                    {"username" : "TestUser", 
                                     "email" : "test@email.com",
                                     "password" : "test",
                                     "password_confirm" : "test2"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
        
        response = self.client.get("/api/users/sign-up/")
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
    
    def test_sign_in_user(self):
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suabyak", 
                                     "password" : "suabo"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], True)
        self.assertEqual(response_dict["message"], "Successfully logged in")
        self.assertEqual(response_dict["userId"], User.objects.all()[0].id)
        
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suaby", 
                                     "password" : "suabo"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
        self.assertEqual(response_dict["message"], "Invalid username or password")
        
        response = self.client.post("/api/users/sign-in/", 
                                    {"username" : "Suabyak", 
                                     "password" : "suaboooo"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
        self.assertEqual(response_dict["message"], "Invalid username or password")
        
        response = self.client.get("/api/users/sign-in/")
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
    
    def test_get_user_data(self):
        response = self.client.get("/api/users/get-user-data/", 
                                    {"id" : User.objects.all()[0].id})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["username"], User.objects.all()[0].username)
        self.assertEqual(response_dict["success"], True)
        
        
        response = self.client.get("/api/users/get-user-data/", 
                                    {"id" : -3})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
        
        
        response = self.client.post("/api/users/get-user-data/", 
                                    {"id" : User.objects.all()[0].id})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["success"], False)
    
    def test_get_users_by_search(self):
        response = self.client.get("/api/users/get-users-by-search/", 
                                    {"search" : "abya"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["users"][0]["username"], User.objects.all()[0].username)
        
        response = self.client.get("/api/users/get-users-by-search/", 
                                    {"search" : "Suabyak"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["users"][0]["username"], User.objects.all()[0].username)
        
        response = self.client.get("/api/users/get-users-by-search/", 
                                    {"search" : "Suabyako"})
        response_dict = dict_from_json_response(response)
        self.assertEqual(response_dict["users"], [])
        
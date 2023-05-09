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
        self.user = User.objects.first()
    
    def test_create_post(self):
        pass
        # response = self.client.post("/api/posts/create/", 
        #                             {"i" : "TestUser", 
        #                              "email" : "test@email.com",
        #                              "password" : "test",
        #                              "password_confirm" : "test"})
        # response_dict = dict_from_json_response(response)
        # self.assertEqual(response_dict["success"], True)
        
        # response = self.client.post("/api/users/sign-up/", 
        #                             {"username" : "TestUser", 
        #                              "email" : "test@email.com",
        #                              "password" : "test",
        #                              "password_confirm" : "test2"})
        # response_dict = dict_from_json_response(response)
        # self.assertEqual(response_dict["success"], False)
        
        # response = self.client.get("/api/users/sign-up/")
        # response_dict = dict_from_json_response(response)
        # self.assertEqual(response_dict["success"], False)
   
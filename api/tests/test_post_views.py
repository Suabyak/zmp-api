from django.test import TestCase, Client
from django.contrib.auth.models import User
from api.models import Post
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
        post = Post(
            body="Lorem ipsum sit dolor amet...",
            user=self.user
        )
        post.save()
        self.assertEqual(Post.objects.filter(body="Lorem ipsum sit dolor amet...").first().id, post.id)
        
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Post, Likes
from api.views.users import get_token_for_user

class TestPostViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        response = self.client.post("/api/users/sign-up/", 
                                    {"username" : "Suabyak", 
                                    "email" : "suaby@email.com",
                                    "password" : "suabo",
                                    "password_confirm" : "suabo"})
        self.user = User.objects.first()
        self.token = f"Bearer {get_token_for_user(self.user)}"
    
    def test_create_post(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""},
                                    **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 532)
    
    def test_get_user_posts(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorua Merleu", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        
        response = self.client.get(f"/api/posts/user-get/{self.user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["posts"]), 2)
        self.assertEqual(response.data["posts"][1]["body"], "Lorua Merleu")

        response = self.client.get(f"/api/posts/user-get/12364567/")
        self.assertEqual(response.status_code, 530)
    
    def test_get_post_by_id(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorua Merleu", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id = response.data['id']
        
        response = self.client.get(f"/api/posts/get/{id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], id)
        self.assertEqual(response.data['body'], "Lorua Merleu")
        
        response = self.client.get(f"/api/posts/get/12364567/")
        self.assertEqual(response.status_code, 533)
        
    def test_update_post(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorua Merleu", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id = response.data['id']
        
        response = self.client.patch(f"/api/posts/update/{id}/", 
                                     {
                                         "body": "Merleu Sorleu"
                                     }, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.filter(id=id).first().body, "Merleu Sorleu")
        
        response = self.client.patch(f"/api/posts/update/12364567/", 
                                     {
                                         "body": "Merleu Sorleu"
                                     }, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 533)
    
    def test_delete_post(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id_wrong_test = response.data["id"]
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorua Merleu", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id = response.data['id']
        
        response = self.client.delete(f"/api/post/{id}/",
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.filter(id=id).first(), None)
        
        response = self.client.delete(f"/api/post/{id_wrong_test}/",
                                    **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 532)
    
    def test_like_post(self):
        
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id = response.data['id']
        
        response = self.client.post(f"/api/post/like/{id}/", 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.filter(id=id).first().get_likes_amount(), 1)
        
        response = self.client.post(f"/api/post/like/{id}/", 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.filter(id=id).first().get_likes_amount(), 0)
        
        response = self.client.post(f"/api/post/like/{id}/",
                                    **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 532)
        
        
    def test_comment_post(self):
        
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        id = response.data['id']
        
        response = self.client.post(f"/api/post/{id}/comment/", 
                                    {"body": "Fajny post :]"},
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(f"/api/post/12364567/comment/", 
                                    {"body": "Fajny post :]"},
                                    **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 530)
        
        response = self.client.post(f"/api/post/{id}/comment/", 
                                    {"body": "Fajny post :]"},
                                    **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 532)
    
    def test_get_feed(self):
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        response = self.client.post("/api/posts/create/", 
                                    {"body": "Lorem ipsum", "file":""}, 
                                    **{"HTTP_AUTHORIZATION" : self.token})
        response = self.client.post(f"/api/user/observe/", 
                            {"id": self.user.id},
                            **{"HTTP_AUTHORIZATION" : self.token})
        response = self.client.get(f"/api/posts/get-feed/",
                            **{"HTTP_AUTHORIZATION" : self.token})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(f"/api/posts/get-feed/",
                            **{"HTTP_AUTHORIZATION" : "Wrong token"})
        self.assertEqual(response.status_code, 532)
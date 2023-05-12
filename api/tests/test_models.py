from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Post, Likes, Comment

class TestModels(TestCase):
    def test_posts_on_user_delete(self):
        User.objects.create_user(username = "Suabyak",
                                email = "mail",
                                password = "paslord")
        user = User.objects.filter(username="Suabyak").first()
        
        post = Post(
            user = user,
            body = "Fajny poscik"
        )
        post.save()
        
        self.assertEqual(len(Post.objects.all()), 1)
        
        user.delete()
        self.assertEqual(len(Post.objects.all()), 0)
    
    def test_likes_on_post_delete(self):
        
        User.objects.create_user(username = "Suabyak",
                                email = "mail",
                                password = "paslord")
        user = User.objects.filter(username="Suabyak").first()
        
        post = Post(
            user = user,
            body = "Fajny poscik"
        )
        post.save()
        
        likes = Likes(
            user=user,
            post=post
        )
        likes.save()
        
        self.assertEqual(len(Likes.objects.all()), 1)
        
        post.delete()
        self.assertEqual(len(Likes.objects.all()), 0)
             
    def test_likes_on_user_delete(self):
        User.objects.create_user(username = "Suabyak",
                                email = "mail",
                                password = "paslord")
        user = User.objects.filter(username="Suabyak").first()
        
        post = Post(
            user = user,
            body = "Fajny poscik"
        )
        post.save()
        
        likes = Likes(
            user=user,
            post=post
        )
        likes.save()
        
        self.assertEqual(len(Likes.objects.all()), 1)
        
        user.delete()
        self.assertEqual(len(Likes.objects.all()), 0)
        
    def test_comments_on_user_delete(self):
        
        User.objects.create_user(username = "Suabyak",
                                email = "mail",
                                password = "paslord")
        user = User.objects.filter(username="Suabyak").first()
        
        post = Post(
            user = user,
            body = "Fajny poscik"
        )
        post.save()
        
        comment = Comment(
            user=user,
            post=post,
            body="komentarian"
        )
        comment.save()
        
        self.assertEqual(len(Comment.objects.all()), 1)
        
        user.delete()
        self.assertEqual(len(Comment.objects.all()), 0)
        
    def test_comments_on_post_delete(self):
        
        User.objects.create_user(username = "Suabyak",
                                email = "mail",
                                password = "paslord")
        user = User.objects.filter(username="Suabyak").first()
        
        post = Post(
            user = user,
            body = "Fajny poscik"
        )
        post.save()
        
        comment = Comment(
            user=user,
            post=post,
            body="komentarian"
        )
        comment.save()
        
        self.assertEqual(len(Comment.objects.all()), 1)
        
        post.delete()
        self.assertEqual(len(Comment.objects.all()), 0)
   
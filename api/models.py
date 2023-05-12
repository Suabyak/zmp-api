from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    
    def get_likes_amount(self):
        return len(Likes.objects.filter(post_id=self.id))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "body": self.body}

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
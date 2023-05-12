from django.db import models
from django.contrib.auth.models import User
from api.utils.models import serialize_model_list, serialize_user

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    
    def get_likes_amount(self):
        return len(Likes.objects.filter(post_id=self.id))

    def serialize(self):
        likes = Likes.objects.filter(post_id=self.id)
        likes = serialize_model_list(likes)
        return {
            "id": self.id,
            "user": serialize_user(self.user),
            "body": self.body,
            "likes": likes,
            "total_likes": self.get_likes_amount()
            }

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def serialize(self):
        return {
            "id": self.id,
            "user": serialize_user(self.user),
            "post_id": self.post.id}

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    
    def serialize(self):
        return {
            "id": self.id,
            "user": serialize_user(self.user),
            "post_id": self.post.id,
            "body": self.body}
    
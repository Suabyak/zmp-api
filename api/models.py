from django.db import models
from django.contrib.auth.models import User
from api.utils.models import serialize_model_list, serialize_user, serialize_data
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    
    def get_likes_amount(self):
        return len(Likes.objects.filter(post_id=self.id))

    def serialize(self):
        likes = Likes.objects.filter(post_id=self.id)
        likes = serialize_model_list(likes)
        return {
            "id": self.id,
            "user": serialize_user(self.user),
            "body": self.body,
            "file": self.image,
            "likes": likes,
            "total_likes": self.get_likes_amount(),
            "created_at": serialize_data(self.created_at)
            }
    
    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        super(Post, self).save(*args, **kwargs)
    

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def serialize(self):
        return self.user.id

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

class Observation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="observator")
    observed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="observed")
    
    def serialize(self):
        return {
            "id": self.id,
            "user": serialize_user(self.user),
            "observed": serialize_user(self.observed)}

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.TextField(blank=True, null=True)
    def serialize(self):
        return self.image
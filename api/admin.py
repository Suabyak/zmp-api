from django.contrib import admin
from models import *

class PostAdmin(Post):
    pass

admin.site.register(Post, PostAdmin)

class LikesAdmin(Likes):
    pass

admin.site.register(Likes, LikesAdmin)

class CommentAdmin(Comment):
    pass

admin.site.register(Comment, CommentAdmin)

class ObservationAdmin(Observation):
    pass

admin.site.register(Observation, ObservationAdmin)

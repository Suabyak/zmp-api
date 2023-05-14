from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    pass

admin.register(Post, PostAdmin)

class LikesAdmin(admin.ModelAdmin):
    pass

admin.register(Likes, LikesAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass

admin.register(Comment, CommentAdmin)

class ObservationAdmin(admin.ModelAdmin):
    pass

admin.register(Observation, ObservationAdmin)

# Register your models here.

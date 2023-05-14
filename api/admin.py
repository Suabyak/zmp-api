from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)

class LikesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Likes, LikesAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)

class ObservationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Observation, ObservationAdmin)

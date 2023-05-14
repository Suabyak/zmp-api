from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post_id"]
    
class LikesAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post"]
    
class ObservationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "observed"]
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(Profile, ProfileAdmin)
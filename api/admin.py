from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Observation)
admin.site.register(Profile)
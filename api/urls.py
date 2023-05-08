from django.urls import path
from .views import users

urlpatterns = [
    path("users/sign-up/", users.sign_up),
    path("users/sign-in/", users.sign_in),
]

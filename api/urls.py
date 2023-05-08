from django.urls import path
from .views import users

urlpatterns = [
    path("users/sign-up/", users.sign_up),
    path("users/sign-in/", users.sign_in),
    path("users/get-user-data/", users.get_user_by_id),
    path("users/get-users-by-search/", users.get_users_by_search),
]

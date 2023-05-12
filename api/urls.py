from django.urls import path
from .views import users

urlpatterns = [
    path("users/sign-up/", users.SingUpView.as_view()),
    path("users/sign-in/", users.SignInView.as_view()),
    path("users/get-user-data/", users.GetUserByIdView.as_view()),
    path("users/get-users-by-search/", users.GetUsersBySearchView.as_view()),
    path("user/", users.GetUserView.as_view()),
    # path("users/logout/", users.LogoutUserView.as_view()),
]

from django.urls import path
from .views import users, posts

urlpatterns = [
    path("users/sign-up/", users.SingUpView.as_view()),
    path("users/sign-in/", users.SignInView.as_view()),
    path("users/get-user-data/", users.GetUserByIdView.as_view()),
    path("users/get-users-by-search/", users.GetUsersBySearchView.as_view()),
    path("user/", users.GetUserView.as_view()),
    
    path("posts/create/", posts.CreatePostView.as_view()),
    path("posts/get/<int:user_id>/", posts.GetUserPostsView.as_view()),
]

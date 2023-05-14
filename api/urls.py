from django.urls import path
from .views import users, posts

urlpatterns = [
    path("users/sign-up/", users.SingUpView.as_view()),
    path("users/sign-in/", users.SignInView.as_view()),
    path("users/get-user-data/", users.GetUserByIdView.as_view()),
    path("users/get-users-by-search/", users.GetUsersBySearchView.as_view()),
    path("user/", users.GetUserView.as_view()),
    path("user/<int:user_id>/comments/", users.GetUserCommentsView.as_view()),
    path("user/observe/", users.ObserveUserView.as_view()),
    path("user/profile/set/", users.SetProfileView.as_view()),
    
    path("posts/create/", posts.CreatePostView.as_view()),
    path("posts/user-get/<int:user_id>/", posts.GetUserPostsView.as_view()),
    path("posts/get/<int:post_id>/", posts.GetPostByIdView.as_view()),
    path("posts/update/<int:post_id>/", posts.UpdatePostView.as_view()),
    path("post/<int:post_id>/", posts.DeletePostView.as_view()),
    path("post/like/<int:post_id>/", posts.LikePostView.as_view()),
    path("post/<int:post_id>/comment/", posts.CommentPostView.as_view()),
    path("post/<int:post_id>/comments/", posts.GetPostCommentsView.as_view()),
    path("posts/get-feed/", posts.GetFeedView.as_view()),
    
]

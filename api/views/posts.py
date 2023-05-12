from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Post
from api.utils.jwt_token import get_user_from_token, WrongTokenException
from api.utils.models import serialize_model_list

class CreatePostView(APIView):
    
    def post(self, request):
        try:
            user = get_user_from_token(request.META.get("token"))
            user = User.objects.filter(id=user["user_id"]).first()
            
            post = Post(
                body=request.data["body"],
                user=user
            )
            
            post.save()
            
            return Response({
                "success": True,
                "message": "Succesfully added post",
                "id": post.id
            })
        except Exception as e:
            return Response({
                "success": False,
            })

class GetUserPostsView(APIView):
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        
        if user is None:
            return Response({
                "success": False
            })
        
        posts = Post.objects.filter(user=user)
        posts = serialize_model_list(posts)
        
        return Response({
            "posts": posts
        })
        
class GetPostByIdView(APIView):
    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "success": False,
                "message": f"There is no post with {post_id} id"
            })

        return Response(post.serialize())

class UpdatePost(APIView):
    def patch(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("token"))
        except WrongTokenException:
            return Response({
                "success": False
            })
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "success": False,
                "message": f"There is no post with {post_id} id"
            })
            
        if post.user.id != user["user_id"]:
            return Response({
                "success": False,
            })
            
        post.body = request.data["body"]
        post.save()
        
        return Response({
            "success": True
        })

class DeletePost(APIView):
    def delete(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("token"))
        except WrongTokenException:
            return Response({
                "success": False
            })
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "success": False,
                "message": f"There is no post with {post_id} id"
            })
        
        post.delete()
        
        return Response({
            "success": True
        })
        
        
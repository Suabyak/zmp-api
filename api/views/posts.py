from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Post, Likes, Comment, Observation
from api.utils.jwt_token import get_user_from_token, WrongTokenException
from api.utils.models import serialize_model_list

class CreatePostView(APIView):
    
    def post(self, request):
        try:
            user = get_user_from_token(request.META.get("Authorization"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=532)
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

class GetUserPostsView(APIView):
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        
        if user is None:
            return Response(status=530)
        
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
                "message": f"There is no post with {post_id} id"
            }, status=533)

        return Response(post.serialize())

class UpdatePostView(APIView):
    def patch(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("Authorization"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=532)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=533)
            
        if post.user.id != user["user_id"]:
            return Response(status=534)
            
        post.body = request.data["body"]
        post.save()
        
        return Response()

class DeletePostView(APIView):
    def delete(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("Authorization"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=532)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=533)
        
            
        if post.user.id != user["user_id"]:
            return Response(status=534)
            
        post.delete()
        
        return Response()
        
class LikePostView(APIView):
    def post(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("Authorization"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=532)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=533)
            
            
        if post.user.id != user["user_id"]:
            return Response(status=534)
        
        likes = Likes.objects.filter(user_id=user["user_id"], post_id=post.id).first()
        if likes is not None:
            likes.delete()
        
            return Response()
            
        likes = Likes(
            post = post,
            user = User.objects.filter(id=user["user_id"]).first()
        )
        likes.save()
        
        return Response()
        
class CommentPostView(APIView):
    def post(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("Authorization"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=532)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)
        
        comment = Comment(
            post = post,
            user = User.objects.filter(id=user["user_id"]).first(),
            body = request.data["body"]
        )
        comment.save()
        
        return Response()


class GetFeedView(APIView):
    def get(self, request):
        try:
            user = get_user_from_token(request.META.get("Authorization"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=532)
        
        observations = Observation.objects.filter(user=user["user_id"])
        observations = serialize_model_list(observations)
        
        posts = Post.objects.none()
        for observation in observations:
            observed_posts = Post.objects.filter(user_id=observation["observed"]["id"])
            posts |= observed_posts
            
        posts = posts.order_by("-created_at")
        posts = serialize_model_list(posts[:50])
        
        return Response({
            "posts": posts
        })
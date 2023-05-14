from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Post, Likes, Comment, Observation
from api.utils.jwt_token import get_user_from_token, WrongTokenException
from api.utils.models import serialize_model_list

class CreatePostView(APIView):
    def post(self, request):
        try:
            request.data["body"]
            request.data["file"]
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=531)
        user = User.objects.filter(id=user["id"]).first()

        post = Post.objects.create(body=request.data["body"],
                                    user=user,
                                    image=request.data["file"])
        
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
        
        return Response(posts)
        
class GetPostByIdView(APIView):
    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)

        return Response(post.serialize())

class UpdatePostView(APIView):
    def patch(self, request, post_id):
        try:
            request.data["body"]
            request.data["file"]
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=531)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)
            
        if post.user.id != user["id"]:
            return Response(status=530)
            
        post.body = request.data["body"]
        post.file = request.data["file"]
        post.save()
        
        return Response()

class DeletePostView(APIView):
    def delete(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=531)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)
        
            
        if post.user.id != user["id"]:
            return Response(status=534)
            
        post.delete()
        
        return Response()
        
class LikePostView(APIView):
    def post(self, request, post_id):
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=531)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)
            
            
        if post.user.id != user["id"]:
            return Response(status=530)
        
        likes = Likes.objects.filter(user_id=user["id"], post_id=post.id).first()
        if likes is not None:
            likes.delete()
        
            return Response()
        
        Likes.objects.create(post = post,
            user = User.objects.filter(id=user["id"]).first())
        
        return Response()
        
class CommentPostView(APIView):
    def post(self, request, post_id):
        try:
            request.data["body"]
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=531)
            
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)
            
        comment = Comment.objects.create(post = post,
            user = User.objects.filter(id=user["id"]).first(),
            body = request.data["body"])
        
        return Response()


class GetFeedView(APIView):
    def get(self, request):
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "message":"Token not provided"}, status=531)
        except WrongTokenException:
            return Response({
                "message":"Wrong token"}, status=531)
        
        observations = Observation.objects.filter(user=user["id"])
        observations = serialize_model_list(observations)
        
        posts = Post.objects.none()
        for observation in observations:
            observed_posts = Post.objects.filter(user_id=observation["observed"]["id"])
            posts |= observed_posts
            
        posts = posts.order_by("-created_at")
        posts = serialize_model_list(posts[:50])
        
        return Response(posts)

class GetPostCommentsView(APIView):
    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id).first()
        
        if post is None:
            return Response({
                "message": f"There is no post with {post_id} id"
            }, status=530)
        
        comments = Comment.objects.filter(post_id=post_id)
        comments = serialize_model_list(comments)

        return Response(comments)
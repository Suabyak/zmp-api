from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Post, Likes, Comment, Observation
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

class UpdatePostView(APIView):
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

class DeletePostView(APIView):
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
        
            
        if post.user.id != user["user_id"]:
            return Response({
                "success": False,
            })
            
        post.delete()
        
        return Response({
            "success": True
        })
        
class LikePostView(APIView):
    def post(self, request, post_id):
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
        
        likes = Likes.objects.filter(user_id=user["user_id"], post_id=post.id).first()
        if likes is not None:
            likes.delete()
        
            return Response({
                "success": True
            })
            
        likes = Likes(
            post = post,
            user = User.objects.filter(id=user["user_id"]).first()
        )
        likes.save()
        
        return Response({
            "success": True
        })
        
class CommentPostView(APIView):
    def post(self, request, post_id):
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
        
        comment = Comment(
            post = post,
            user = User.objects.filter(id=user["user_id"]).first(),
            body = request.data["body"]
        )
        comment.save()
        
        return Response({
            "success": True
        })


class GetFeedView(APIView):
    def get(self, request):
        try:
            user = get_user_from_token(request.META.get("token"))
        except KeyError:
            return Response({
                "success":False, 
                "message":"Token not provided"})
        except WrongTokenException:
            return Response({
                "success":False, 
                "message":"Wrong token"})
        
        observations = Observation.objects.filter(user=user["user_id"])
        observations = serialize_model_list(observations)
        
        posts = list()
        for observation in observations:
            observed_posts = Post.objects.filter(user_id=observation["observed"]["id"])
            posts.extend(serialize_model_list(observed_posts))
        print(posts)
        return Response({
            "success": True,
            "posts": posts
        })
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.utils.jwt_token import get_user_from_token, get_token_for_user, WrongTokenException
from api.models import Comment
from api.utils.models import serialize_model_list


class SingUpView(APIView):    
    def post(self, request):
        if (request.data["password"] != request.data["password_confirm"]):  
            return Response({
                "success":False, 
                "message":"Passwords are not the same"})
        
        User.objects.create_user(username = request.data["username"],
                                email = request.data["email"],
                                password = request.data["password"])
        
        return Response({
            "success":True, 
            "message":"Successfully signed up"})


class SignInView(APIView):       
    def post(self, request):
        user = authenticate(username = request.data["username"], 
                            password = request.data["password"])

        if user is None:
            return Response({
                "success":False, 
                "message":"Invalid username or password"})
        token = get_token_for_user(user)
        
        return Response(
            {"success":True, 
             "message":"Successfully logged in",
             "user_id":user.id,
             "token":token})
        
class GetUserByIdView(APIView):
    def get(self, request):        
        try:
            user = User.objects.get(id=request.GET.get("id"))
        except User.DoesNotExist:
            return Response({
                "success":False, 
                "message":f"There is no User with id {request.GET.get('id')}"})
        
        return Response({
            "success":True, 
            "username":user.username
        })

class GetUsersBySearchView(APIView):
    def get(self, request):  
        users = User.objects.filter(username__contains=request.GET.get("search"))
        
        users_lsit = list()
        for user in users:
            users_lsit.append({"username":user.username, 
                            "id":user.id})
            
        return Response({
            "users":users_lsit
        })

class GetUserView(APIView):
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
        
        if user is None:
            return Response({
                "success":False, 
                "message":"Unauthenticated"})
        user["success"] = True 
        return Response(user)

class GetUserCommentsView(APIView):
    def get(self, request, user_id):
        comments = Comment.objects.filter(user_id=user_id)
        comments = serialize_model_list(comments)
        
        return Response({
            "comments": comments
        })
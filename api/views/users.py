from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from django.contrib.auth.models import User
import jwt, datetime, zmp_api.settings as settings

def get_token_for_user(user):
    payload = {
        "id":user.id,
        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iat":datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    
    return token

def get_user_from_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    
    return User.objects.filter(id=payload["id"]).first()

class SingUpView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
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
        login(request, user)
        token = get_token_for_user(user)
        response = Response(
            {"success":True, 
             "message":"Successfully logged in",},
            headers={"token":token})
        
        return response
        
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
            user = get_user_from_token(request.headers["token"])
        except KeyError:
            return Response({
                "success":False, 
                "message":"Token not provided"})
        except:
            return Response({
                "success":False, 
                "message":"Wrong token"})
            
        if user is None:
            return Response({
                "success":False, 
                "message":"Unauthenticated"})
        
        return Response({
            "success":True,
            "username":user.username,
            "email":user.email,
            "id":user.id
        })

class LogoutUserView(APIView):
    def post(self, request):
        response = Response({
            "success":True,
            "message":"Successfully logout"
        })
        if not request.user.is_authenticated:
            return Response({
                "success":False,
                "message":"Not logged in"
            })
        logout(request)
        return response
        
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import jwt, zmp_api.settings as settings
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny

def get_token_for_user(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    
    return token

def get_user_from_token(token):
    payload = api_settings.JWT_DECODE_HANDLER(token)
    
    return payload


class SingUpView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        # print(request.data)
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
    permission_classes = (AllowAny,)
    
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
        except:
            return Response({
                "success":False, 
                "message":"Wrong token"})
        
        if user is None:
            return Response({
                "success":False, 
                "message":"Unauthenticated"})
        user["success"] = True 
        return Response(user)

# class LogoutUserView(APIView):
#     def post(self, request):
        
#         if not request.user.is_authenticated:
#             return Response({
#                 "success":False,
#                 "message":"Not logged in"
#             })
#         logout(request)
#         return Response({
#             "success":True,
#             "message":"Successfully logout"
#         })
        
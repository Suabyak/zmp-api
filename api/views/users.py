from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.jwt_token import get_user_from_token, get_token_for_user, WrongTokenException
from api.models import Comment, Observation, Profile
from api.utils.models import serialize_model_list, serialize_user_list


class SingUpView(APIView):    
    def post(self, request):
        try:
            request.data["username"]
            request.data["email"]
            request.data["password"]
            request.data["password_confirm"]
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        if (request.data["password"] != request.data["password_confirm"]):  
            return Response({
                "success":False, 
                "message":"Passwords are not the same"},
                            status=530)
        user = User.objects.create_user(username = request.data["username"],
                                email = request.data["email"],
                                password = request.data["password"])
        Profile.objects.create(user=user, image="")
        return Response({
            "success":True, 
            "message":"Successfully signed up"})


class SignInView(APIView):       
    def post(self, request):
        try:
            request.data["username"]
            request.data["password"]
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        user = authenticate(username = request.data["username"], 
                            password = request.data["password"])

        if user is None:
            return Response({
                "success":False, 
                "message":"Invalid username or password"},
                            status=530)
        token = get_token_for_user(user)
        
        return Response(
            {"success":True, 
             "message":"Successfully logged in",
             "id":user.id,
             "token":token})
        
class GetUserByIdView(APIView):
    def get(self, request): 
        try:
            request.GET.get("id")
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
                   
        try:
            user = User.objects.get(id=request.GET.get("id"))
        except User.DoesNotExist:
            return Response({
                "success":False, 
                "message":f"There is no User with id {request.GET.get('id')}"},
                            status=530)
        
        return Response({
            "success":True, 
            "username":user.username
        })

class GetUsersBySearchView(APIView):
    def get(self, request):  
        try:
            request.GET.get("search")
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        users = User.objects.filter(username__contains=request.GET.get("search"))
        users = serialize_user_list(users)
            
            
        return Response(users)

class GetUserView(APIView):
    def get(self, request):
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "success":False, 
                "message":"Token not provided"},
                            status=531)
        except WrongTokenException:
            return Response({
                "success":False, 
                "message":"Wrong token"},
                            status=531)
        
        if user is None:
            return Response({
                "success":False, 
                "message":"Unauthenticated"},
                            status=530)
        user["success"] = True 
        return Response(user)

class GetUserCommentsView(APIView):
    def get(self, request, user_id):
        comments = Comment.objects.filter(user_id=user_id)
        comments = serialize_model_list(comments)
        
        return Response(comments)

class ObserveUserView(APIView):
    def post(self, request):
        try:
            request.data["id"]
        except KeyError:
            return Response({
                "success":False,
            "message":"Wrong data send"
            }, status = 530)
            
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "success":False, 
                "message":"Token not provided"},
                            status=531)
        except WrongTokenException:
            return Response({
                "success":False, 
                "message":"Wrong token"},
                            status=531)
        to_observe = User.objects.filter(id=request.data["id"]).first()
        
        if to_observe is None:
            return Response({
                "success":False, 
                "message":f"There is no User with id {request.data['id']}"},
                            status=530)
        
        observation = Observation.objects.filter(user_id=user["id"], observed_id=to_observe.id).first()
        if observation is not None:
            observation.delete()
            
            return Response({
                "success":True, 
            })
        
        Observation.objects.create(
            user=User.objects.filter(id=user["id"]).first(),
            observed=to_observe)
        
        return Response({
            "success":True, 
        })


class SetProfileView(APIView):
    def post(self, request):
        try:
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
                "success":False, 
                "message":"Token not provided"},
                            status=531)
        except WrongTokenException:
            return Response({
                "success":False, 
                "message":"Wrong token"},
                            status=531)

        profile = Profile.objects.filter(user_id=user["id"]).first()
        profile.image = request.data["file"]
        profile.save()
        
        return Response({
            "success":True, 
        })


class GetObservedView(APIView):
    def get(self, request):
        try:
            user = get_user_from_token(request.META.get("HTTP_AUTHORIZATION"))
        except KeyError:
            return Response({
                "success":False, 
                "message":"Token not provided"},
                            status=531)
        except WrongTokenException:
            return Response({
                "success":False, 
                "message":"Wrong token"},
                            status=531)
    
        observed = Observation.objects.filter(user_id=user["id"])
        observed = serialize_model_list(observed)
        
        return Response(observed)
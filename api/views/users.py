from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import serializers


def sign_up(request):
    if (request.method == "GET"):
        return JsonResponse({
            "success":False, 
            "message":"Forbidden method"})
        
    if (request.POST.get("password") != request.POST.get("password_confirm")):  
        return JsonResponse({
            "success":False, 
            "message":"Passwords are not the same"})
    
    user = User.objects.create_user(username = request.POST.get("username"),
                             email = request.POST.get("email"),
                             password = request.POST.get("password"))
    
    return JsonResponse({
        "success":True, 
        "message":"Successfully signed up"})
    
def sign_in(request):
    if (request.method == "GET"):
        return JsonResponse({
            "success":False, 
            "message":"Forbidden method"})
    
    user = authenticate(username = request.POST.get("username"), 
                        password = request.POST.get("password"))

    if user is None:
        return JsonResponse({
            "success":False, 
            "message":"Invalid username or password"})
    
    return JsonResponse({
        "success":True, 
        "message":"Successfully logged in",
        "userId":user.id})
    
def get_user_by_id(request):
    if (request.method == "POST"):
        return JsonResponse({
            "success":False, 
            "message":"Forbidden method"})
    
    try:
        user = User.objects.get(id=request.GET.get("id"))
    except User.DoesNotExist:
        return JsonResponse({
            "success":False, 
            "message":f"There is no User with id {request.GET.get('id')}"})
    
    return JsonResponse({
        "success":True, 
        "username":user.username
    })
    
def get_users_by_search(request):
    if (request.method == "POST"):
        return JsonResponse({
            "success":False, 
            "message":"Forbidden method"})
    
    users = User.objects.filter(username__contains=request.GET.get("search"))
    
    users_lsit = list()
    for user in users:
        users_lsit.append({"username":user.username, 
                          "id":user.id})
        
    return JsonResponse({
        "users":users_lsit
    })
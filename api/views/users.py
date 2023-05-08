from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
    
    
    
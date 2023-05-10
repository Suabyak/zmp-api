from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response

class GetTokenView(APIView):   
    def get(self, request):
        csrf_token = get_token(request)
        
        return Response({
            "csrf_token": csrf_token
        })
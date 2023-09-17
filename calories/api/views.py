from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, CaloriesSerializer


class EndPoints(APIView):
    def get(self, request):
        data = [
            '/api/signup',
            '/api/login',
            '/api/logout',
            '/api/users',
            'api/users/:user_id',
            'api/calories',
            'api/calories/:calories_id'
        ]
        return Response(data)


class RegisterUser(APIView):
    pass

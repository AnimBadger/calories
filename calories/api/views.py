from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, CaloriesSerializer
from rest_framework import status
from .models import UserDetail, CaloriesInput
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


class EndPoints(APIView):
    permission_classes = [IsAuthenticated]

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
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.isValid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = UserDetail.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')

        return Response({'message': 'login success'})

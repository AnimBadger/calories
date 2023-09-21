from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, CaloriesSerializer
from rest_framework import status
from .models import UserDetail, CaloriesInput
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import os
import requests


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


app_id = os.getenv('APPLICATION_ID')
app_key = os.getenv('APPLICATION_KEY')


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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Calories(APIView):
    queryset = CaloriesInput.objects.all()
    serializer_class = CaloriesInput
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CaloriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'number_of_calories' not in serializer.validated_data or serializer.validated_data['number_of_calories'] is None:
            food_name = serializer.validated_data['name']
            nutritionix_api_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
            headers = {
                "x-app-id": app_id,
                "x-app-key": app_key,
                "Content-Type": "application/json",
            }
            params = {
                'query': food_name
            }
            response = requests.post(
                nutritionix_api_url, headers=headers, json=params)
            if response.status_code == 200:
                nutrition_data = response.json()
                serializer.validated_data['number_of_calories'] = (
                    nutrition_data['foods'][0]['nf_calories'])
            else:
                raise Response({'error': 'Could not find data'},
                               status=status.HTTP_404_NOT_FOUND)

        serializer.validated_data['user'] = request.user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

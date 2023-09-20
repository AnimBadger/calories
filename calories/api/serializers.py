from rest_framework import serializers
from .models import UserDetail, CaloriesInput
import os
import requests

app_id = os.getenv('APPLICATION_ID')
app_key = os.getenv('APPLICATION_KEY')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['username', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None and len(password) >= 8:
            instance.set_password(password)
            instance.save()
        else:
            raise serializers.ValidationError(
                {'password': 'Password must be at least 8 characters long'})
        return instance


class CaloriesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        model = CaloriesInput
        fields = ['name', 'number_of_calories',
                  'description', 'date', 'time', 'username']

    def validate(self, data):
        if data['number_of_calories'] < 0:
            raise serializers.ValidationError(
                {'Error': 'Number of calories cannot be less than 0'})
        return data

    def create(self, validated_data):
        username = validated_data.pop('username', None)

        user = UserDetail.objects.get(username=username)

        if 'number_of_calories' not in validated_data or validated_data['number_of_calories'] is None:
            food_name = validated_data['name']

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
                validated_data['number_of_calories'] = (
                    nutrition_data['foods'][0]['nf_calories'])
            else:
                raise serializers.ValidationError(
                    {'Error': 'Unable to fetch calories from Nutritionix API'})

        validated_data['user'] = user
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance

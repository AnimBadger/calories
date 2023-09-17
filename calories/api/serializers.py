from rest_framework import serializers
from .models import UserDetail, CaloriesInput


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
    class Meta:
        model = CaloriesInput
        fields = ['name', 'number_of_calories',
                  'description', 'date', 'time']

        def validate(self, data):
            if data['number_of_calories'] < 0:
                raise serializers.ValidationError(
                    {'Error': 'Number of calories can not be less than 0'})
            return data

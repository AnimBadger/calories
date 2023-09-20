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
    username = serializers.CharField(write_only=True)
    number_of_calories = serializers.FloatField(required=False)

    class Meta:
        model = CaloriesInput
        fields = ['name', 'number_of_calories',
                  'description', 'date', 'time', 'username']

    def validate(self, data):
        number_of_calories = data.get('number_of_calories')

        if number_of_calories is not None and number_of_calories < 0:
            raise serializers.ValidationError(
                {'number_of_calories': 'Number of calories cannot be less than 0'})

        return data

    def create(self, validated_data):
        username = validated_data.pop('username', None)

        user = UserDetail.objects.get(username=username)

        validated_data['user'] = user
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance

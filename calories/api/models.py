from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserDetail(AbstractUser):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=False)

    def __str__(self):
        return f'{self.username}'


class CaloriesInput(models.Model):
    user = models.ForeignKey(
        UserDetail, on_delete=models.CASCADE, to_field='username')
    name = models.CharField(max_length=50)
    number_of_calories = models.FloatField()
    description = models.TextField(null=False, blank=False)
    date = models.DateField(default=timezone.now().date())
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'

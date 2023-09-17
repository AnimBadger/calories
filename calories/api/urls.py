from django.urls import path
from .views import EndPoints, RegisterUser, LoginUser

urlpatterns = [
    path('', EndPoints.as_view()),
    path('api/login', LoginUser.as_view()),
    path('api/signup', RegisterUser.as_view()),
]

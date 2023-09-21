from django.urls import path
from .views import EndPoints, RegisterUser, Calories, MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', EndPoints.as_view()),
    path('api/signup', RegisterUser.as_view()),
    path('api/login', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/calories', Calories.as_view()),
]

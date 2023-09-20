from django.urls import path
from .views import EndPoints, RegisterUser, LoginUser, Calories
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', EndPoints.as_view()),
    path('api/login', LoginUser.as_view()),
    path('api/signup', RegisterUser.as_view()),
    # path('api/token/', CustomTokenObtainPairView.as_view(),
    #     name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/calories', Calories.as_view()),
]

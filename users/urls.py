from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', views.listCreateUsersView.as_view(), name='users-list-create'),
    path('users/<int:id>/', views.retrieveUpdateDeleteUserView.as_view(), name='users-datail'),
    path('register/', views.registerUserView.as_view(), name='register-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

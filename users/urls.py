from django.urls import path
from users import views 


urlpatterns = [ 
  path('users/', views.listCreateUsersView.as_view()), 
  path('users/<str:username>/', views.retrieveUpdateDeleteUserView.as_view())
]
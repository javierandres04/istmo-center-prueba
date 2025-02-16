from django.urls import path
from users import views 


urlpatterns = [ 
  path('users/', views.listCreateUsersView.as_view(), name='users-list-create'), 
  path('users/<int:id>/', views.retrieveUpdateDeleteUserView.as_view(), name='users-datail')
]
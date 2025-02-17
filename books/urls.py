from books.views import ListCreateBooksView, retrieveUpdateDeleteBookView
from django.urls import path


urlpatterns = [
    path('books/', ListCreateBooksView.as_view(), name='books-list-create'),
    path('books/<int:id>/', retrieveUpdateDeleteBookView.as_view(), name='books-detail'),
]
from books.views import ListCreateBooksView, retrieveUpdateDeleteBookView, ReturnBook
from books.views.book_loan_views import ListCreateLoans
from django.urls import path


urlpatterns = [
    path('books/', ListCreateBooksView.as_view(), name='books-list-create'),
    path('books/<int:id>/', retrieveUpdateDeleteBookView.as_view(),name='books-detail'),
    path('loans/', ListCreateLoans.as_view(), name='book-loans'),
    path('returns/', ReturnBook.as_view(), name='return-book')
]

from rest_framework import serializers
from books.models import Book, BookLoan
from users.serializers.user_serializers import SimpleUserSerializer


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'genre', 'available']
        extra_kwargs = {'id': {'read_only': True}}


class BookLoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_isbn = serializers.CharField(source='book.isbn', read_only=True)
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = BookLoan
        fields = ['id', 'loan_date', 'return_date', 'returned',
                  'book_id', 'book_title', 'book_isbn', 'user_id', 'user_email']
        extra_kwargs = {'id': {'read_only': True}, 'loan_date': {'read_only': True},
                        'return_date': {'read_only': True}, 'returned': {'read_only': True}}

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, default='Novel')
    isbn = models.CharField(max_length=17, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.book.title} - {self.user.email}'
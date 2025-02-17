from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from books.models import Book
from users.models import User


class BookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            role=User.Role.ADMIN
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890',
            genre='Test Genre',
            available=True
        )

    def test_list_books(self):
        url = reverse('books-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_list_books_pagination(self):
        Book.objects.all().delete()
        for i in range(15):
            Book.objects.create(
                title=f'Test Book {i}',
                author='Test Author',
                isbn=f'1234{i}',
                genre='Test Genre',
                available=True
            )

        url = reverse('books-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('total_pages', response.data)
        self.assertIn('current_page', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)

    def test_list_books_pagination_limit(self):
        Book.objects.all().delete()
        for i in range(15):
            Book.objects.create(
                title=f'Test Book {i}',
                author='Test Author',
                isbn=f'1234{i}',
                genre='Test Genre',
                available=True
            )

        url = reverse('books-list-create')
        response = self.client.get(url + '?limit=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

    def test_list_books_pagination_limit_page(self):
        Book.objects.all().delete()
        for i in range(15):
            Book.objects.create(
                title=f'Test Book {i}',
                author='Test Author',
                isbn=f'1234{i}',
                genre='Test Genre',
                available=True
            )

        url = reverse('books-list-create')
        response = self.client.get(url + '?limit=10&page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['current_page'], 2)
        self.assertEqual(response.data['total_pages'], 2)
        self.assertNotEqual(response.data['previous'], None)

    def test_list_books_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('books-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_books_empty(self):
        Book.objects.all().delete()
        url = reverse('books-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.data["results"])

    def test_get_book_detail_ok(self):
        url = reverse('books-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_get_book_detail_not_found(self):
        url = reverse('books-detail', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_book_detail_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('books-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_ok(self):
        url = reverse('books-list-create')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '45678',
            'genre': 'New Genre',
            'available': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('books-list-create')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '45678',
            'genre': 'New Genre',
            'available': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('books-list-create')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '45678',
            'genre': 'New Genre',
            'available': True
        }
        response = self.client.post(url, data)
        books = Book.objects.all()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(books.count(), 1)

    def test_create_book_bad_Request(self):
        url = reverse('books-list-create')
        data = {
            'title': 'New Book',
            'isbn': '45678',
            'genre': 'New Genre',
            'available': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_patch_ok(self):
        url = reverse('books-detail', args=[self.book.id])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_update_book_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('books-detail', args=[self.book.id])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('books-detail', args=[self.book.id])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        book = Book.objects.get(id=self.book.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(book.title, 'Test Book')

    def test_update_book_put_ok(self):
        url = reverse('books-detail', args=[self.book.id])
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'isbn': '1234567890',
            'genre': 'Updated Genre',
            'available': False
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')
        self.assertEqual(self.book.genre, 'Updated Genre')
        self.assertEqual(self.book.available, False)

    def test_update_book_put_bad_request(self):
        url = reverse('books-detail', args=[self.book.id])
        data = {
            'title': 'Updated Title',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book_not_found(self):
        url = reverse('books-detail', args=[3])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book_ok(self):
        url = reverse('books-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_not_found(self):
        url = reverse('books-detail', args=[3])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('books-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('books-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 1)

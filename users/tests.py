
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from users.models import User


class usersTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            role=User.Role.ADMIN
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        url = reverse('users-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_users_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('users-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_user(self):
        url = reverse('users-list-create')
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'Test User',
            'role': User.Role.USER
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email='test@test.com').email, 'test@test.com')
        self.assertEqual(User.objects.get(email='test@test.com').name, 'Test User')
        self.assertEqual(User.objects.get(email='test@test.com').role, User.Role.USER)
    
    def test_create_user_bad_request(self):
        url = reverse('users-list-create')
        data = {
            'password': 'testpass123',
            'name': 'Test User',
            'role': User.Role.USER
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('users-list-create')
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'Test User',
            'role': User.Role.USER
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('users-list-create')
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'Test User',
            'role': User.Role.USER
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 1)

    def test_get_user_detail(self):
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['name'], self.user.name)
        self.assertEqual(response.data['role'], self.user.role)
    
    def test_get_user_detail_not_found(self):
        url = reverse('users-detail', args=[3])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_detail_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_detail_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_patch(self):
        url = reverse('users-detail', args=[self.user.id])
        data = {
            'email': 'test@test.com',
            'password': 'testpass2',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.check_password('testpass2'), True)
    
    def test_update_user_patch_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('users-detail', args=[self.user.id])
        data = {
            'email': 'test@test.com',
            'password': 'testpass2',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.check_password('testpass123'), True)

    def test_update_user_patch_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('users-detail', args=[self.user.id])
        data = {
            'email': 'test@test.com',
            'password': 'testpass2',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.check_password('testpass123'), True)

    def test_update_uiser_not_found(self):
        url = reverse('users-detail', args=[3])
        data = {
            'email': 'test@test.com',
            'password': 'testpass2',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'test@test.com')

    def test_user_delete(self):
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_user_delete_unauthorized(self):
        self.client.force_authenticate(user=None)
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_delete_not_admin(self):
        self.user.role = User.Role.USER
        self.user.save()
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 1)
    
    def test_user_delete_not_found(self):
        url = reverse('users-detail', args=[3])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 1)

    def test_get_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_token_bad_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'testuser2@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_token_bad_request(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'testuser2@example.com',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_refresh_token(self):
        refresh_url = reverse('token_refresh')
        token_url = reverse('token_obtain_pair')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(token_url, data, format='json')
        token = response.data['refresh']

        response = self.client.post(refresh_url, {'refresh': token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertNotIn('refresh', response.data)



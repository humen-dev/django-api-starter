from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tools.tests import USER_PASSWORD, BaseAPITestCase


class TestRegisterView(BaseAPITestCase):
    url = reverse('auth-register')

    def test_success(self):
        payload = {
            'email': 'new@example.com',
            'password': 'strongpassword',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(self.url, payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == payload['email']
        assert response.data['first_name'] == payload['first_name']
        assert 'password' not in response.data

    def test_sets_httponly_auth_cookies(self):
        payload = {'email': 'new@example.com', 'password': 'strongpassword'}
        response = self.client.post(self.url, payload)

        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies
        assert response.cookies['access_token']['httponly']
        assert response.cookies['refresh_token']['httponly']

    def test_duplicate_email_returns_400(self):
        user = self.create_user()
        response = self.client.post(self.url, {'email': user.email, 'password': 'strongpassword'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short_returns_400(self):
        response = self.client.post(self.url, {'email': 'new@example.com', 'password': 'short'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_email_returns_400(self):
        response = self.client.post(self.url, {'password': 'strongpassword'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestLoginView(BaseAPITestCase):
    url = reverse('auth-login')

    def setUp(self):
        self.user = self.create_user()

    def test_success(self):
        response = self.client.post(self.url, {'email': self.user.email, 'password': USER_PASSWORD})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == self.user.email
        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies

    def test_invalid_password_returns_400(self):
        response = self.client.post(self.url, {'email': self.user.email, 'password': 'wrongpassword'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_nonexistent_email_returns_400(self):
        response = self.client.post(self.url, {'email': 'nobody@example.com', 'password': USER_PASSWORD})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inactive_user_returns_400(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, {'email': self.user.email, 'password': USER_PASSWORD})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestLogoutView(BaseAPITestCase):
    url = reverse('auth-logout')

    def setUp(self):
        self.user = self.create_user()
        self.authenticate(self.user)

    def test_success(self):
        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.cookies['access_token'].value == ''
        assert response.cookies['refresh_token'].value == ''

    def test_blacklists_refresh_token(self):
        refresh = self.set_refresh_cookie(self.user)
        self.client.post(self.url)

        client = APIClient()
        client.cookies['refresh_token'] = str(refresh)
        response = client.post(reverse('auth-refresh'))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_without_refresh_cookie_returns_204(self):
        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_unauthenticated_returns_401(self):
        response = APIClient().post(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenRefreshView(BaseAPITestCase):
    url = reverse('auth-refresh')

    def setUp(self):
        self.user = self.create_user()

    def test_success(self):
        self.set_refresh_cookie(self.user)
        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.cookies
        assert 'refresh_token' in response.cookies

    def test_no_refresh_cookie_returns_401(self):
        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_token_returns_401(self):
        self.client.cookies['refresh_token'] = 'not.a.valid.token'
        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestMeView(BaseAPITestCase):
    url = reverse('auth-me')

    def setUp(self):
        self.user = self.create_user(first_name='Test', last_name='User')
        self.authenticate(self.user)

    def test_success(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == self.user.email
        assert response.data['first_name'] == self.user.first_name
        assert response.data['last_name'] == self.user.last_name
        assert 'password' not in response.data

    def test_unauthenticated_returns_401(self):
        response = APIClient().get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

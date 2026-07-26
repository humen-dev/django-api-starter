from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

USER_PASSWORD = 'testpassword123'


class BaseAPITestCase(APITestCase):
    def create_user(self, email='test@example.com', password=USER_PASSWORD, **kwargs):
        from apps.users.models import User

        return User.objects.create_user(email=email, password=password, **kwargs)

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.cookies['access_token'] = str(refresh.access_token)

    def set_refresh_cookie(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.cookies['refresh_token'] = str(refresh)
        return refresh

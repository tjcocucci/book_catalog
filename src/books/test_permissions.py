from django.urls import reverse
from django.test import TestCase, RequestFactory
from unittest.mock import patch, Mock
from rest_framework.test import APIClient
from .permissions import AuthServerPermission
from django.conf import settings
from .models import Genre, Book


class AuthServerPermissionTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.permission = AuthServerPermission()
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            isbn="1234567890123",
            title="Test Book",
            author="Author Name",
            stock=10,
            price=19.99,
        )
        self.book.genres.add(self.genre)
        self.url = reverse("book-list-create")
        settings.AUTH_SERVER_URL = "http://fake-auth-server.com"

    @patch("requests.get")
    def test_permission_with_valid_token(self, mock_get):
        mock_response = Mock()
        mock_response.ok = True
        mock_get.return_value = mock_response

        request = self.factory.get("/books/", HTTP_AUTHORIZATION="Bearer valid_token")
        has_permission = self.permission.has_permission(request, None)

        self.assertTrue(has_permission)
        mock_get.assert_called_once_with(
            f"{settings.AUTH_SERVER_URL}/session/",
            headers={"Authorization": "Bearer valid_token"},
        )

    @patch("requests.get")
    def test_permission_with_invalid_token(self, mock_get):
        mock_response = Mock()
        mock_response.ok = False
        mock_get.return_value = mock_response

        request = self.factory.get("/books/", HTTP_AUTHORIZATION="Bearer invalid_token")
        has_permission = self.permission.has_permission(request, None)

        self.assertFalse(has_permission)
        mock_get.assert_called_once_with(
            f"{settings.AUTH_SERVER_URL}/session/",
            headers={"Authorization": "Bearer invalid_token"},
        )

    @patch("requests.get")
    def test_permission_without_token(self, mock_get):
        request = self.factory.get("/books/")
        has_permission = self.permission.has_permission(request, None)

        self.assertFalse(has_permission)
        mock_get.assert_not_called()

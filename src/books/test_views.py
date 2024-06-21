from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
from .models import Genre, Book, InventoryItem
from .serializers import GenreSerializer, BookSerializer, InventoryItemSerializer


class GenreViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Fiction")
        self.url = reverse('genre-list-create')

    @patch('books.permissions.AuthServerPermission.has_permission', return_value=True)
    def test_get_genres(self, mock_permission):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Fiction')

    @patch('books.permissions.AuthServerPermission.has_permission', return_value=True)
    def test_create_genre(self, mock_permission):
        data = {'name': 'Non-Fiction'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)
        self.assertTrue(Genre.objects.filter(name='Non-Fiction').exists())


class BookViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(isbn="1234567890123", title="Test Book", author="Author Name", stock=10, price=19.99)
        self.book.genres.add(self.genre)
        self.url = reverse('book-list-create')

    @patch('books.permissions.AuthServerPermission.has_permission', return_value=True)
    def test_get_books(self, mock_permission):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')

    @patch('books.permissions.AuthServerPermission.has_permission', return_value=True)
    def test_create_book(self, mock_permission):
        data = {
            'isbn': "9876543210987",
            'title': "New Book",
            'author': "New Author",
            'stock': 5,
            'price': 15.99,
            'genres': [{'name': self.genre.name}]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertTrue(Book.objects.filter(title='New Book').exists())


class InventoryViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.inventory_item = InventoryItem.objects.create(stock=10, price=19.99)
        self.url = reverse('inventory-list-create')

    @patch('books.permissions.AuthServerPermission.has_permission', return_value=True)
    def test_get_inventory(self, mock_permission):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['stock'], 10)
        self.assertEqual(response.data[0]['price'], '19.99')

    @patch('books.permissions.AuthServerPermission.has_permission', return_value=True)
    def test_create_inventory(self, mock_permission):
        data = {
            'stock': 5,
            'price': 15.99
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)
        self.assertTrue(InventoryItem.objects.filter(stock=5).exists())
        self.assertTrue(InventoryItem.objects.filter(price=15.99).exists())

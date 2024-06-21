from django.test import TestCase
from .models import Genre, Book

class GenreModelTest(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, "Fiction")

    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Fiction")

class BookModelTest(TestCase):

    def setUp(self):
        self.genre = Genre.objects.create(name="Fiction")
        self.book = Book.objects.create(isbn="1234567890123", title="Test Book", author="Author Name", stock=10, price=19.99)
        self.book.genres.add(self.genre)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Author Name")
        self.assertEqual(self.book.stock, 10)
        self.assertEqual(self.book.price, 19.99)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_book_genres(self):
        self.assertIn(self.genre, self.book.genres.all())

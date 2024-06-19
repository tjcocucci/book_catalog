from .models import Genre, Book, InventoryItem
from .serializers import GenreSerializer, BookSerializer, InventoryItemSerializer
from .permissions import AuthServerPermission
from rest_framework import generics


class GenreListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AuthServerPermission]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthServerPermission]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AuthServerPermission]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthServerPermission]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class InventoryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AuthServerPermission]
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer


class InventoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthServerPermission]
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

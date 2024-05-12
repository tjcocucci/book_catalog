from django.urls import path
from .views import (
    GenreListCreateAPIView,
    GenreRetrieveUpdateDestroyAPIView,
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    InventoryListCreateAPIView,
    InventoryRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("genres/", GenreListCreateAPIView.as_view(), name="genre-list-create"),
    path(
        "genres/<int:pk>/",
        GenreRetrieveUpdateDestroyAPIView.as_view(),
        name="genre-detail",
    ),
    path("books/", BookListCreateAPIView.as_view(), name="book-list-create"),
    path(
        "books/<int:pk>/",
        BookRetrieveUpdateDestroyAPIView.as_view(),
        name="book-detail",
    ),
    path(
        "inventory/", InventoryListCreateAPIView.as_view(), name="inventory-list-create"
    ),
    path(
        "inventory/<int:pk>/",
        InventoryRetrieveUpdateDestroyAPIView.as_view(),
        name="inventory-detail",
    ),
]

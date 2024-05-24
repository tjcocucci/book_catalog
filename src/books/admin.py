from django.contrib import admin
from .models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "price", "stock")
    list_filter = ("genres",)
    search_fields = ("title", "author", "isbn")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)

from django.contrib import admin
from .models import Book, Genre


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "price", "stock")
    list_filter = ("genres",)
    search_fields = ("title", "author", "isbn")


admin.site.register(Book, BookAdmin)
admin.site.register(Genre)

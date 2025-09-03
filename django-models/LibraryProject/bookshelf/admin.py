from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book

# Customize how Book is displayed in the admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these columns
    list_filter = ('publication_year', 'author')  # filter options on the right
    search_fields = ('title', 'author')  # adds a search box

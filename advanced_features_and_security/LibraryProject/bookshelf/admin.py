# Register your models here.
from django.contrib import admin
from .models import Book
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Customize how Book is displayed in the admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these columns
    list_filter = ('publication_year', 'author')  # filter options on the right
    search_fields = ('title', 'author')  # adds a search box

class CustomUserAdmin(UserAdmin):
    # Display these fields in the admin list
    list_display = ("username", "email", "date_of_birth", "is_staff", "is_superuser")

    # Add date_of_birth and profile_photo to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )

    # for the create user page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("date_of_birth", "profile_photo")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


# View all books (requires can_view)
@permission_required("bookshelf.can_view", raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, "bookshelf/view_books.html", {"books": books})

# Add a new book (requires can_create)
@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    # Implementation for creating a book
    return render(request, "bookshelf/add_book.html")

# Edit book (requires can_edit)
@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    # Implementation for editing a book
    return render(request, "bookshelf/edit_book.html")

# Delete book (requires can_delete)
@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    # Implementation for deleting a book
    return render(request, "bookshelf/delete_book.html")


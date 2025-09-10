from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from django.db.models import Q

# Create your views here.

# View all books (requires can_view)
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
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


def search_books(request):
    query = request.GET.get("q", "")
    results = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    )
    return render(request, "bookshelf/book_list.html", {"books": results, "query": query})


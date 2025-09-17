from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter


# Create router instance
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    # Router-generated CRUD routes
    path('', include(router.urls)),
]


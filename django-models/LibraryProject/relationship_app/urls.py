from django.urls import path
from .views import list_books, LibraryDetailView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path("books/", list_books, name="list_books"),  
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path("login/", CustomLoginView.as_view(), template_name="login"),
    path("logout/", CustomLogoutView.as_view(), template_name="logout"),
    path("register/", register, template_name="register"),
]



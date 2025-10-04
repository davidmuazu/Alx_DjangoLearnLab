from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth using Django’s built-ins
    path("login/",  auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logout.html"), name="logout"),

    # Custom
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]

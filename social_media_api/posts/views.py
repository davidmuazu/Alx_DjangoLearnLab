from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, permissions

# Custom permission
from rest_framework.permissions import IsAuthenticatedOrReadOnly

User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow full access to object owner; others have read-only access.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author', None) == request.user


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FeedView(generics.ListAPIView):
    """
    Returns posts from users the current user follows, ordered by newest first.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        # if user follows nobody, returns empty queryset
        follows = user.following.all()
        return Post.objects.filter(author__in=follows).order_by('-created_at')

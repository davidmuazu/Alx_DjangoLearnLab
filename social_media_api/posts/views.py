from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


User = get_user_model()


# Custom permission
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.GenericAPIView):
    """
    Returns posts from users that the current user follows,
    ordered by creation date (newest first).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)



class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        if request.user == post.author:
            return Response({"detail": "You cannot like your own post."}, status=status.HTTP_400_BAD_REQUEST)

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification for post author if author != liker
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=str(post.pk),
            )

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)




class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like_qs = Like.objects.filter(user=request.user, post=post)
        if not like_qs.exists():
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like_qs.delete()

        # Delete related notifications
        Notification.objects.filter(
            recipient=post.author,
            actor=request.user,
            verb__icontains="liked",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=str(post.pk)
        ).delete()

        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)

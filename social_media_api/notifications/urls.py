from django.urls import path
from .views import NotificationListView, MarkAllReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),  #for /api/notifications
    path('mark-read/', MarkAllReadView.as_view(), name='notifications-mark-read'),
]

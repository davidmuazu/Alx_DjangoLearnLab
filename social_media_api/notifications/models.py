from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import AppConfig
# Create your models here.



User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actor_notifications")
    verb = models.CharField(max_length=255)  # e.g., 'liked', 'followed', 'commented'
    # Generic target (could be a Post, Comment, etc.)
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")
    unread = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Notification for {self.recipient}: {self.actor} {self.verb}"

class NotificationsConfig(AppConfig):
    name = "notifications"

    def ready(self):
        import notifications.signals
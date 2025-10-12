from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from notifications.models import Notification
from accounts.models import User 

@receiver(m2m_changed, sender=User.following.through)
def following_changed(sender, instance, action, pk_set, **kwargs):
    # When someone follows a user, create notification for the followed user
    if action == "post_add":
        for followed_id in pk_set:
            followed_user = User.objects.get(pk=followed_id)
            Notification.objects.create(
                recipient=followed_user,
                actor=instance,
                verb="followed you",
                target_content_type=None,
                target_object_id=""
            )

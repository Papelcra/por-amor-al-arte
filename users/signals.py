from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from artists.models import Artist

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'artist':
            Artist.objects.create(user=instance, stage_name=instance.username)
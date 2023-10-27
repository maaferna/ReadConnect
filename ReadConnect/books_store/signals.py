# To automatically create a UserProfile instance for a user created through Django Allauth
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # The create_user_profile function checks if a new user has been created (created is True). If so, it creates a UserProfile instance associated with that user.
    if created:
        UserProfile.objects.create(user=instance)
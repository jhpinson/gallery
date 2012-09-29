from .models import Profile
#Post signal to autocreate profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)   
from django.db import models
import uuid 

def get_upload_path(instance, filename):
    return 'avatars/' + str(uuid.uuid4()) + filename.split('.')[-1]


class Profile(models.Model):
    
    user = models.OneToOneField("auth.User")
    avatar = models.ImageField(null=True, upload_to=get_upload_path)
    
    

from django.db import models
import uuid
from helpers.rest.models import AjaxModelHelper
from sorl.thumbnail.shortcuts import get_thumbnail

def get_upload_path(instance, filename):
    return 'avatars/' + str(uuid.uuid4()) + filename.split('.')[-1]


class Profile(AjaxModelHelper, models.Model):

    user = models.OneToOneField("auth.User")
    avatar = models.ImageField(null=True, upload_to=get_upload_path)


    def toJSON(self):
        
        small = get_thumbnail(self.avatar.file, "100x100", upscale=True)
        
        return {
                'first_name' : self.user.first_name,
                'last_name' : self.user.last_name,
                'avatar' : {
                                'small' : small.url
                                }
                }
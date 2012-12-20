from django.contrib.auth.models import User
from medias.models import Album, create_media
import os
from django.db.utils import IntegrityError
import datetime
from middleware.request import set_current_user


def get_jobs(last=0):

    import_path = "/home/virtualenv/photos-nastux/"
    
    for image in Image.objects.all():
        yield image.pk

def handle_job(pk):
    
    image = Image.objects.get(pk=pk)
    
    try:
        image.generate_thumbnail(size)
        image.save()
    except IOError,e:
        print "IOERROR deleting file", image.pk, image.file.url, image.delete()


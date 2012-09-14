from django.core.management.base import BaseCommand
import os
from structures.models import Album

from PIL import Image as PILImage
from medias.models.image import Image
import hashlib
from django.db.utils import IntegrityError
from PIL.ExifTags import TAGS
from dateutil.parser import parse
from django.contrib.auth.models import User
import datetime
from django.core.files.base import ContentFile

def _hash(data):
    r =  hashlib.sha1(data).hexdigest()
    return r

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        user = User.objects.get(pk=1)
        
        extensions = {}
        
        for rep, dirs, files in os.walk(args[0]):
            
            for file in files:
                ext = file.lower().split('.')[-1]
                try:
                    extensions[ext] += 1
                except KeyError:
                    extensions[ext] = 1
        
        print extensions
            
            
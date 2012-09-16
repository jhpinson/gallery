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
        
        import_path = args[0]
        user = User.objects.get(pk=1)
        
        root_category = Album.objects.get( parent_id = 1, created_by=user)
       
        for rep, dirs, files in os.walk(args[0]):
            
            # mpg, mov, avi
            
            images = [file for file in files if file.lower().split('.')[-1] in ['jpeg', 'jpg', 'png']]
            
            if len(images) > 0:
                path = rep.replace(import_path, '')
                
                if len(path) == 0:
                    cat = root_category
                    created = False
                else:
                    p = path.split('/')[-1]
                    cat, created = Album.objects.get_or_create(name=p, parent=root_category, created_by = user, modified_by=user)
                    
                if not created:
                    continue
                
                for image in images:
                    
                    img_path = "%s/%s" % (rep, image)
                    
                    f = open(img_path, 'r')
                    try:
                        img = PILImage.open(f)
                        new_image = Image(created_by=user, modified_by=user)
                        exif = img._getexif()
                        if exif is not None:
                            for tag, value in exif.items():
                                decoded = TAGS.get(tag, tag)
                                if  decoded == 'DateTimeOriginal':
                                    new_image.date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                                    break
                        
                            
                        name = image
                        new_image.name = name
                        new_image.album=cat
                        
                        if new_image.date is None:
                            new_image.date= datetime.datetime.fromtimestamp(os.path.getmtime(img_path))
                        
                        f.seek(0)
                        new_image.file.save(
                                      name
                                      , ContentFile(f.read()), save=True)
                        
                    except IntegrityError,e:
                        continue
                    
                    except Exception,e:
                        print e
                        continue
                    
                    f.close()
                    
                    
                    
                print cat.pk, len(images)
            
            
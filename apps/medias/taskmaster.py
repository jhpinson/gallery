from django.contrib.auth.models import User
from structures.models import Album
from medias.models import Image, Video
import os
from PIL import Image as PILImage
from django.db.utils import IntegrityError
from PIL.ExifTags import TAGS
import datetime
from django.core.files.base import ContentFile

def get_jobs(last=0):
    
    import_path = "/home/virtualenv/photos-nastux/"
    
    user = User.objects.get(pk=1)
    root_category = Album.objects.get( parent_id = 1, created_by=user)
   
    for rep, dirs, files in os.walk(import_path):
        
        # mpg, mov, avi
        
        images = [file for file in files if file.lower().split('.')[-1] in ['jpeg', 'jpg', 'png', 'mpg', 'avi', 'mov']]
        
        if len(images) > 0:
            path = rep.replace(import_path, '')
            
            if len(path) == 0:
                cat = root_category
                created = False
            else:
                p = path.split('/')[-1]
                cat, created = Album.objects.get_or_create(name=p, parent=root_category, created_by = user, modified_by=user)
                
            for image in images:
                yield cat.pk, rep, image, user.pk
                
def handle_job(data):
    album_pk, rep, name, user_pk = data
    
    image_path = "%s/%s" % (rep, name)
    
    f = open(image_path, 'r')
    
    if name.lower().split('.')[-1] in ['mpg', 'avi', 'mov']:
        clazz = Video
    else:
        clazz = Image
    
    obj =  clazz(created_by_id=user_pk, modified_by_id=user_pk, name=name, album_id=album_pk)
    
    try:
        
        if clazz == Image:
        
            img = PILImage.open(f)
            
            exif = img._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    decoded = TAGS.get(tag, tag)
                    if  decoded == 'DateTimeOriginal':
                        obj.date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        break
        
            
        
        
        if obj.date is None:
            obj.date= datetime.datetime.fromtimestamp(os.path.getmtime(image_path))
        
        f.seek(0)
        obj.file.save(
                      name
                      , ContentFile(f.read()), save=True)
        
    except IntegrityError,e:
        pass
    
    except Exception,e:
        print e
        
    
    f.close()


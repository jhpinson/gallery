from django.core.management.base import BaseCommand
import os
from structure.models import Category

from StringIO import StringIO
from PIL import Image as PILImage
import uuid
from django.core.files.base import ContentFile
from medias.models.image import Image
import hashlib
from django.db.utils import IntegrityError
from PIL.ExifTags import TAGS
from dateutil.parser import parse
from django.core.exceptions import ObjectDoesNotExist

def _hash(data):
    r =  hashlib.sha1(data).hexdigest()
    return r

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        root = args[0]
        
        root_category, created = Category.objects.get_or_create(name='root', defaults={'name' : 'root'})
        
        for rep, dirs, files in os.walk(args[0]):
            
            images = [file for file in files if file.lower().split('.')[-1] in ['jpeg', 'jpg', 'png']]
            
            if len(images) > 0:
                path = rep.replace(root, '')
                
                if len(path) == 0:
                    cat = root_category
                else:
                    parent = root_category
                    for p in path.split('/'):
                        try:
                            cat = Category.objects.get(name=p, parent=parent)
                        except ObjectDoesNotExist:
                            cat = Category(name=p, parent=parent)
                            cat.save()
                        
                        parent = cat
                        
            
                for image in images:
                    f = open("%s/%s" % (rep, image), 'r')
                    img = PILImage.open(f)
                    
                    output_file = StringIO()
                    img.save(output_file, "PNG")
                    
                    h = _hash(output_file.getvalue())
                    try:
                        
                        # exif datas
                        dateTimeOriginal = None
                        exif = img._getexif()
                        for tag, value in exif.items():
                            decoded = TAGS.get(tag, tag)
                            if  decoded == 'DateTimeOriginal':
                                dateTimeOriginal = value
                                
                        
                        #@TODO si dateTimeOriginal is None, prendre la date de modification du fichier
                        name = "%s.png" % '.'.join(image.split('.')[:-1]) 
                        name = name.lower()
                        
                        img = Image(name=name, hash=h, category=cat, date=parse(dateTimeOriginal))
                        
                        
                        img.file.save(
                                      name
                                      , ContentFile(output_file.getvalue()), save=True)
                    except IntegrityError,e:
                        pass
                    else:
                        print "%s/%s" % (rep, image)
                        
                    f.close()
                    
                    
                    
                print cat, len(images)
            
            
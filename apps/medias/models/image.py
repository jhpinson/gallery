from .media import Media

from django.db.models import permalink
from medias.models.mixins.models import ThumbAccessors
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from medias.models.mixins.manager import PermissionManager
import subprocess
from django.conf import settings
from subprocess import CalledProcessError
from PIL import Image as PILImage
from PIL.ExifTags import TAGS
import datetime

class ImageQuerySet(PermissionManager, QuerySet):
    pass

class Image(ThumbAccessors, Media):
    
    objects = PassThroughManager.for_queryset_class(ImageQuerySet)()
        
    def save(self, *args, **kwargs):
        
        if self._state.adding:
            img = PILImage.open(self.file.path)
            exif = img._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    decoded = TAGS.get(tag, tag)
                    if  decoded == 'DateTimeOriginal':
                        self.meta_date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        break
        
        super(Image, self).save(*args, **kwargs)
        
    def generate_thumbnails(self):
        self.generate_thumbnail('small', self.file.file)
        self.generate_thumbnail('medium', self.file.file)
        self.generate_thumbnail('large', self.file.file)
    
    
    def toJSON(self):
        
        return {
                'id' : self.pk,
                'name' : self.name,
                'description' : self.description,
                'date' : str(self.date),
                'is_an_album' : self.is_an_album,
                'parent_album' : self.parent_album.pk if self.parent_album is not None else None,
                'thumbnails' : {
                                'small' : self.thumbnail_small(),
                                'medium' : self.thumbnail_medium(),
                                'large' : self.thumbnail_large()
                                }}
     
            
    @permalink
    def get_absolute_uri(self):
        
        return 'media_view', None, {'pk': self.pk}
    
    def rotate(self, value):
        
        ext = self.original_file.path.split('.')[-1]
        abs_dest_path = self.original_file.path.replace(ext, 'modified.' + ext)
        args = ['convert',self.file.path,'-rotate',value, abs_dest_path]
        try:
            ret  = subprocess.check_call(args)
        except CalledProcessError, e:
            print e
            raise 
        self.custom_file = abs_dest_path.replace(settings.MEDIA_ROOT, '')
        self.clean_thumbnails()
        self.generate_thumbnails()
        self.save()
            
    class Meta:
        app_label = 'medias'
        verbose_name = 'Photo'
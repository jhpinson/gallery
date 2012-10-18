from .media import Media

from django.db.models import permalink
from medias.models.mixins.models import ThumbAccessors
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from medias.models.mixins.manager import PermissionManager
import subprocess
from django.conf import settings
from subprocess import CalledProcessError

class ImageQuerySet(PermissionManager, QuerySet):
    pass

class Image(ThumbAccessors, Media):
    
    objects = PassThroughManager.for_queryset_class(ImageQuerySet)()
        
    def generate_thumbnails(self):
        self.generate_thumbnail('small', self.file.file)
        self.generate_thumbnail('medium', self.file.file)
        self.generate_thumbnail('large', self.file.file)
    
        
            
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
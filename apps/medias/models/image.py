from .media import Media

from django.db.models import permalink
from medias.models.mixins.models import ThumbAccessors
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from medias.models.mixins.manager import PermissionManager
from medias.models.videos import Video

class ImageQuerySet(PermissionManager, QuerySet):
    pass

class Image(ThumbAccessors, Media):
    objects = PassThroughManager.for_queryset_class(ImageQuerySet)()
    
    def upload_path(self, filename):
        return '%s/%s' % ('/'.join([c.name for c in self.album.get_ancestors()] + [self.album.name]), filename)
    
    def generate_thumbnails(self):
        self.generate_thumbnail('small', self.file.file)
        self.generate_thumbnail('medium', self.file.file)
        self.generate_thumbnail('large', self.file.file)
    
            
    @permalink
    def get_absolute_uri(self):
        
        return 'media_view', None, {'pk': self.pk}
    
    class Meta:
        app_label = 'medias'
        verbose_name = 'Photo'
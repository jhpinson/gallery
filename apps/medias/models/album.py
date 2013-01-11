from django.db import models
from medias.models import Media, Thumbnail, Image, Video

from middleware.request import get_current_user
from medias.models.mixins.manager import PermissionManager
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager

class AlbumQuerySet(PermissionManager, QuerySet):
    
    pass

    
    

class Album(Media):
    
    _cached_album_thumbnail = None
    
    end_date = models.DateTimeField(null=True)
    
    image_count = models.PositiveIntegerField(default=0)
    video_count = models.PositiveIntegerField(default=0)
    
    objects = PassThroughManager.for_queryset_class(AlbumQuerySet)()
    
    
    def get_ancestors(self):
        
        ancestors = []
        current = self.parent_album
        while current is not None:
            ancestors.insert(0,current)
            current = current.parent_album
          
        return ancestors
        
    
    def get_children(self):
        
        return self.medias
    
    
            
    @property
    def can_play_diaporama(self):
        return self.medias.models(Image, Video).exists()
           
    
    
    
    @models.permalink
    def get_absolute_uri(self):
        return 'album_view', None, {'pk': self.pk}
    
        
    def consolidate_count(self):
        
        self.image_count = Image.objects.filter(parent_album=self, status=Media.STATUSES.published).count()
        self.video_count = Video.objects.filter(parent_album=self, status=Media.STATUSES.published).count()
        
        if self.image_count > 0 or self.video_count > 0:
            date = Media.objects.filter(parent_album=self, status=Media.STATUSES.published).order_by('date')[0].date
            self.meta_date = date
        else:
            self.meta_date = None
            self.end_date = None
        
        thumb_media_qs = Media.objects.models(Image, Video).filter(parent_album=self, status=Media.STATUSES.published).exclude(url_small=None)
        if thumb_media_qs.count() > 0:
            thumb_media = Media.objects.models(Image, Video).filter(parent_album=self, status=Media.STATUSES.published).exclude(url_small=None)[0]
            self.url_small = thumb_media.url_small
            self.width_small = thumb_media.width_small
            self.height_small = thumb_media.height_small
        else:
            self.url_small = None
            self.width_small = None
            self.height_small = None
        
        self.save()
        
        
        
    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'medias'
        verbose_name = 'Album'

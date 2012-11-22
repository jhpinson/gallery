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
    
    def toJSON(self):
        data = {
                'id' : self.pk,
                'name' : self.name,
                'description' : self.description,
                'is_an_album' : self.is_an_album,
                'image_count' : self.image_count,
                'video_count' : self.video_count,
                'parent_album' : self.parent_album.pk if self.parent_album is not None else None,
                'thumbnails' : {'small' : self.album_thumbnail.toJSON()}}
            
        return data
    
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
    def album_thumbnail(self):
        
        if self._cached_album_thumbnail is None:
            try:
                self._cached_album_thumbnail =  Thumbnail.objects.get(media_id=self.get_children().models(Image, Video)[0], size='small')
            except Exception:
                self._cached_album_thumbnail = False
        
        return self._cached_album_thumbnail
            
    @property
    def can_play_diaporama(self):
        return self.medias.models(Image, Video).exists()
            
    """
    @property
    def display_name(self):
        if self.is_user_root is True:
            
            if self.owner == get_current_user():
                return 'Mes albums'
            else:
                return self.owner.get_full_name()
        else:
            return self.name
    """
    
    
    
    @models.permalink
    def get_absolute_uri(self):
        return 'album_view', None, {'pk': self.pk}
    
        
    def consolidate_count(self):
        
        self.image_count = Image.objects.filter(parent_album=self).count()
        self.video_count = Video.objects.filter(parent_album=self).count()
        
        if self.image_count > 0 or self.video_count > 0:
            date = Media.objects.filter(parent_album=self).order_by('file_creation_date')[0].date
            self.meta_date = date
        else:
            self.meta_date = None
            self.end_date = None
        self.save()
        
        
        
    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'medias'
        verbose_name = 'Album'
from django.db import models
from medias.models import Media, Thumbnail, Image, Video

from middleware.request import get_current_user

class Album(Media):
    end_date = models.DateTimeField(null=True)
    
    album_count = models.PositiveIntegerField(default=0)
    image_count = models.PositiveIntegerField(default=0)
    video_count = models.PositiveIntegerField(default=0)
    
    def get_ancestors(self):
        
        ancestors = []
        current = self.parent_album
        while current is not None:
            ancestors.insert(0,current)
            current = current.parent_album
          
        return ancestors
        
    
    def get_children(self):
        
        return self.medias
    
    def default_thumbnail(self):
        try:
            return Thumbnail.objects.get(media_id=self.get_children().models(Image)[0], size='small')
        except Exception,e:
            print e
            return '/pix.gif'
            
    
    @property
    def display_name(self):
        if self.is_user_root is True:
            
            if self.owner == get_current_user():
                return 'Mes albums'
            else:
                return self.owner.get_full_name()
        else:
            return self.name
    
    @property
    def is_root(self):
        return self.name=='root' and self.parent_album is None
    
    @property
    def is_user_root(self):
        try:
            return self.parent_album.is_root
        except:
            return False
    
    @models.permalink
    def get_absolute_uri(self):
        return 'album_view', None, {'pk': self.pk}
    
        
    def consolidate_count(self):
        
        self.album_count = Album.objects.filter(parent_album=self).count()
        self.image_count = Image.objects.filter(parent_album=self).count()
        self.video_count = Video.objects.filter(parent_album=self).count()
        
        if self.album_count > 0 or self.image_count > 0 or self.video_count > 0:
            self.start_date = Media.objects.filter(parent_album=self).order_by('date')[0].date
            self.end_date = Media.objects.filter(parent_album=self).order_by('-date')[0].date
        
        self.save()
        
        
        
    def __unicode__(self):
        if self.is_user_root:
            return self.owner.get_full_name()
        else:
            return self.name

    class Meta:
        app_label = 'medias'

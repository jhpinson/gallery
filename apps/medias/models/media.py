
from django.db import models
from django.contrib.contenttypes.models import ContentType
from model_utils.managers import PassThroughManager, InheritanceQuerySet
from model_utils import Choices
from helpers.mixins import ChangeTrackMixin
from filehashfield.fields import FileHashField
from datetime import datetime
from sorl.thumbnail.shortcuts import get_thumbnail
from django.conf import settings
from sorl.thumbnail import delete

class MediaQuerySet(InheritanceQuerySet):
            
    def models(self, *models):
        return self.filter(real_type__in=[ContentType.objects.get_for_model(model) for model in models])
        
    def get_subclass(self, *args, **kwargs):
        return self.select_subclasses().get(*args, **kwargs)

class Media(ChangeTrackMixin, models.Model):
    
    def upload_path(self, filename):
        path = "/".join([str(self.created_by.pk), str(self.date.year), "%02d" % self.date.month, "%02d" % self.date.day, filename])
        return path
    
    name = models.CharField(max_length=512)
    description = models.TextField(max_length=2048)
    date = models.DateTimeField(default=datetime.now)
    
    file = FileHashField(upload_to=upload_path, hash_field='hash', max_length=1024, null=True)
    hash = models.CharField(max_length=40, null=True)
    
    real_type = models.ForeignKey(ContentType, editable=False, null=True)
    
    parent_album = models.ForeignKey('medias.Album', related_name='medias', null=True)
    
    is_an_album = models.PositiveSmallIntegerField()
    
    objects = PassThroughManager.for_queryset_class(MediaQuerySet)()
    
    
    def get_absolute_uri(self):
        return self.cast().get_absolute_uri()
    
    @property
    def owner(self):
        return self.created_by
    
    def generate_thumbnails(self):
        pass
    
    def generate_thumbnail(self, size, f):
        image = get_thumbnail(f, "%sx%s" % (settings.THUMBNAIL_SIZES[size]['width'], settings.THUMBNAIL_SIZES[size]['height']), upscale=True)
        
        data = {'url' : image.url, 'width':image.width, 'height':image.height}
        
        if not Thumbnail.objects.filter(media=self, size=size).exists():
            thumb = Thumbnail(media=self, size=size, **data)
            thumb.save()
        
        return data
    
    def save(self, *args, **kwargs):
        
        created = False
        if self._state.adding:
            self.real_type = self._get_real_type()
            created = True
            
            self.is_an_album = 1 if self.real_type.model == 'album' else 0
            
        super(Media, self).save(*args, **kwargs)
        
        if created and self.parent_album is not None:
                self.parent_album.consolidate_count()
        
        
    def delete(self, *args, **kwargs):
        
        try:
            delete(self.file.file)
        except IOError:
            pass
        self.file.delete(save=False)
        
        super(Media, self).delete(*args, **kwargs)
        
    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)
    
    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'medias'
        #unique_together=('hash', 'album')
        ordering=['-is_an_album', 'date']
        
class Thumbnail(models.Model):
    
    SIZES = Choices('small', 'medium', 'large')
    
    media = models.ForeignKey(Media, related_name='thumbnails')
    
    size = models.CharField(max_length=10, choices=SIZES, default=SIZES.small)
    
    url = models.CharField(max_length=1024)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    
    class Meta:
        app_label = 'medias'
        unique_together=('media','size')
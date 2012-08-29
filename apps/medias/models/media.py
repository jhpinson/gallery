
from django.db import models
from django.contrib.contenttypes.models import ContentType
from model_utils.managers import PassThroughManager, InheritanceQuerySet
from django.core.urlresolvers import  reverse
from sorl.thumbnail.shortcuts import get_thumbnail
from model_utils import Choices
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class MediaQuerySet(InheritanceQuerySet):
            
    def models(self, *models):
        return self.filter(real_type__in=[ContentType.objects.get_for_model(model) for model in models])
        
    def get_subclass(self, *args, **kwargs):
        return self.select_subclasses().get(*args, **kwargs)

class Media(models.Model):

    name = models.CharField(max_length=512)
    description = models.TextField(max_length=2048)
    
    real_type = models.ForeignKey(ContentType, editable=False, null=True)
    
    category = models.ForeignKey('structure.Category')
    
    objects = PassThroughManager.for_queryset_class(MediaQuerySet)()
    
    date = models.DateTimeField(null=True)
    hash = models.CharField(max_length=40)
    
    def __init__(self, *args, **kwargs):
        self._cache = {}
        super(Media, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        
        if self._state.adding:
            self.real_type = self._get_real_type()
            
        super(Media, self).save(*args, **kwargs)
    
    def __getattr__(self, name):
        
        if name[:10] == 'thumbnail_':
            
            if self._cache.get(name, None) is None:
            
                size = name[10:]
                data = {}
                try:
                    thumb = self.thumbnails.get(size=size)
                    data['url'] = thumb.url
                    data['width'] = thumb.width
                    data['height'] = thumb.height
                    data['exists'] = True
                    self._cache[name] = data
                except ObjectDoesNotExist:
                    data['url'] = reverse('generate_thumbnail_view', kwargs={'pk' : self.pk, 'size' : size})
                    data['width'] = settings.THUMBNAIL_SIZES[size]['width']
                    data['height'] = None
                    data['exists'] = False
                    self._cache[name] = data
            
            return self._cache[name]
            
        else:
            return super(Media, self).__getattr__(self, name)
    
    
    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)
    
    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        app_label = 'medias'
        unique_together=('hash', 'category')
        
        
class Thumbnail(models.Model):
    
    SIZES = Choices('small', 'medium', 'large')
    
    media = models.ForeignKey(Media, related_name='thumbnails')
    
    size = models.CharField(max_length=10, choices=SIZES, default=SIZES.small)
    
    url = models.CharField(max_length=1024)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    
    class Meta:
        app_label = 'medias'
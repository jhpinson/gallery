
from django.db import models
from django.contrib.contenttypes.models import ContentType
from model_utils.managers import PassThroughManager, InheritanceQuerySet
from model_utils import Choices
from helpers.mixins import ChangeTrackMixin
from filehashfield.fields import FileHashField
from sorl.thumbnail.shortcuts import get_thumbnail
from django.conf import settings
from sorl.thumbnail import delete
from medias.models.mixins.manager import PermissionManager
from django.db.models.fields.files import FileField
from helpers.rest.models import AjaxModelHelper
from jsonfield.fields import JSONField
#from cacheops.invalidation import invalidate_obj, invalidate_all
import datetime
class MediaQuerySet(PermissionManager, InheritanceQuerySet):

    def models(self, *models):
        return self.filter(real_type__in=[ContentType.objects.get_for_model(model) for model in models])

    def get_subclass(self, *args, **kwargs):
        return self.select_subclasses().get(*args, **kwargs)

class Media(ChangeTrackMixin, AjaxModelHelper, models.Model):

    def upload_path_original(self, filename):
        path = "/".join([str(self.created_by.pk), str(self.date.year), "%02d" % self.date.month, "%02d" % self.date.day, filename])
        return path

    def modified_upload_path(self, filename):
        path = str(self.original_file).split('.')
        return "%s.modified.%s" % ('.'.join(path[:-1]), path[-1])

    STATUSES = Choices('published', 'failed', 'deleted')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUSES.published)

    name = models.CharField(max_length=512)
    description = models.TextField(max_length=2048, null=True, blank=True)

    date = models.DateTimeField(default=datetime.datetime.now) # used date
    file_creation_date = models.DateTimeField(null=True) # if self.file, the file creation date
    meta_date = models.DateTimeField(null=True) # a computed date or exif date
    
    remove_date = models.DateTimeField(null=True) 
    
    original_file = FileHashField(upload_to=upload_path_original, hash_field='hash', max_length=1024, null=True)
    custom_file = FileField(upload_to= modified_upload_path, null=True)

    hash = models.CharField(max_length=40, null=True)

    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    parent_album = models.ForeignKey('medias.Album', related_name='medias', null=True, blank=True)

    is_an_album = models.PositiveSmallIntegerField()
    
    url_small = models.CharField(max_length=1024, null=True)
    width_small = models.PositiveIntegerField(null=True)
    height_small = models.PositiveIntegerField(null=True)
    
    url_medium = models.CharField(max_length=1024, null=True)
    width_medium = models.PositiveIntegerField(null=True)
    height_medium = models.PositiveIntegerField(null=True)
    
    url_large = models.CharField(max_length=1024, null=True)
    width_large = models.PositiveIntegerField(null=True)
    height_large = models.PositiveIntegerField(null=True)
    
    data = JSONField(null=True)
    
    objects = PassThroughManager.for_queryset_class(MediaQuerySet)()
    
    
    def __init__(self, *args, **kwargs):
        super(Media, self).__init__(*args, **kwargs)
        self._keep_init = {'parent_album_id' : self.__dict__.get('parent_album_id'), 'status' : self.__dict__.get('status')}
        
    def toJSON(self):
        from medias.models import Video
        data = {
                'id' : self.pk,
                'name' : self.name,
                'description' : self.description,
                'is_an_album' : self.is_an_album,
                'parent_album' : self.parent_album.pk if self.parent_album is not None else None}
        #data['absolute_url'] = "/toto" #self.get_absolute_uri()
        data['owner'] = {'name' : self.created_by.get_full_name(), 'id' : self.created_by.get_profile().pk}
        data['date'] = self.date.strftime('%Y-%m-%dT%H:%M:%S')
        data['remove_date'] = self.remove_date.strftime('%Y-%m-%dT%H:%M:%S') if self.remove_date is not None else None
        data['status'] = self.status
        data['url_small'] = self.url_small
        data['width_small'] = self.width_small
        data['height_small'] = self.height_small
        data['url_medium'] = self.url_medium
        data['width_medium'] = self.width_medium
        data['height_medium'] = self.height_medium
        #data['url_large'] = self.url_large
        #data['width_large'] = self.width_large
        #data['height_large'] = self.height_large
        
        if self.real_type.model in ['video', 'image']:
            data['original_file'] = self.original_file.url
        
        data['type'] = self.real_type.model
        
        if self.is_an_album:
            
            data['image_count'] = self.image_count
            data['video_count'] = self.video_count
          
        if self.real_type.model == 'video':
            data['video_status'] = self.video_status
            
            if self.video_status == Video.VIDEO_STATUSES.done:
                data['versions'] = {'webm' : self.video_versions.all()[0].file.url} 
            
        return data
        
        
    
    @property
    def file(self):
        return self.custom_file or self.original_file

    def get_position(self):
        from ..models import Image, Video
        qs = [ r[0] for r in self.parent_album.medias.models(Image, Video).values_list('pk')]
        return qs.index(self.pk )

    def get_absolute_uri(self):
        return self.cast().get_absolute_uri()

    @property
    def owner(self):
        return self.created_by

    def clean_thumbnails(self):
        for size in ['small', 'medium', 'large']:
            setattr(self, 'url_%s' % size, None)
            setattr(self, 'width_%s' % size, None)
            setattr(self, 'height_%s' % size, None)
            
        
        try:
            delete(self.original_file.file, delete_file=False)
        except (IOError, ValueError):
            pass

        try:
            if self.custom_file:
                delete(self.custom_file.file, delete_file=False)
        except (IOError, ValueError):
            pass

    def generate_thumbnails(self):
        pass

    def generate_thumbnail(self, size, f=None):

        if f is None:
            f = self.file.file

        if getattr(self, 'url_%s' %size, None) is None:
            options = settings.THUMBNAIL_SIZES[size].get('options', {})
            
            image = get_thumbnail(f, "%sx%s" % (settings.THUMBNAIL_SIZES[size]['width'], settings.THUMBNAIL_SIZES[size]['height']), **options)
            setattr(self, 'url_%s' % size, image.url)
            setattr(self, 'width_%s' % size, image.width)
            setattr(self, 'height_%s' % size, image.height)
            
        if not isinstance(f, basestring):
            f.close()

    def save(self, *args, **kwargs):
        
        created = False
        if self._state.adding:
            self.real_type = self._get_real_type()
            created = True

            self.is_an_album = 1 if self.real_type.model == 'album' else 0
            
        if self.meta_date is not None:
            self.date = self.meta_date
        elif self.file_creation_date is not None:
            self.date = self.file_creation_date
        else:
            self.date = self.created_at
        
        if not created:
            
            if self.status == Media.STATUSES.deleted:
                if self._keep_init['status'] != self.status:
                    self.remove_date = datetime.datetime.now() + datetime.timedelta(days=2)
            else:
                self.remove_date = None
            
            self.data = self.toJSON()
                
        super(Media, self).save(*args, **kwargs)
        
        if created:
            self.data = self.toJSON()
            self.save()
        
        #invalidate_obj(self)
        #invalidate_obj(Media.objects.get(pk=self.pk))
        
        if self._keep_init.get('parent_album_id', None) is not None:
            Media.objects.get(pk=self._keep_init.get('parent_album_id')).cast().consolidate_count()
        
        if self.parent_album is not None:
            self.parent_album.consolidate_count()


    def delete(self, *args, **kwargs):
        if not self.is_an_album:
            self.clean_thumbnails()
            self.original_file.delete(save=False)
            if self.custom_file:
                self.custom_file.delete(save=False)
        else:
            Media.objects.filter(parent_album=self).delete()
        super(Media, self).delete(*args, **kwargs)
        
        if self.parent_album is not None:
            self.parent_album.consolidate_count()
        
    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'medias'
        unique_together=('hash', 'parent_album')
        ordering=['-is_an_album', 'date']

class Thumbnail(models.Model):

    SIZES = Choices('small', 'medium', 'large')

    media = models.ForeignKey(Media, related_name='thumbnails')

    size = models.CharField(max_length=10, choices=SIZES, default=SIZES.small)

    url = models.CharField(max_length=1024)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    
    def toJSON(self):
        return {'url' : self.url,
                 'width' : self.width,
                 'height' : self.height
      }
    
    class Meta:
        app_label = 'medias'
        unique_together=('media','size')

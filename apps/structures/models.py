from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from helpers.mixins import ChangeTrackMixin
from middleware.request import get_current_user
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class Album( MPTTModel):
    
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=512, null=True, blank=True)
    parent = TreeForeignKey('self',  related_name='children', null=True)
    
    created_at = AutoCreatedField('created')
    modified_at = AutoLastModifiedField('modified')
    
    created_by = models.ForeignKey("auth.User", default=get_current_user, related_name="create_by_%(class)s_set", editable=False, null=True)
    modified_by = models.ForeignKey("auth.User", default=get_current_user, related_name="update_by_%(class)s_set", editable=False, null=True)
    
    images_count = models.PositiveIntegerField(default=0)
    album_count = models.PositiveIntegerField(default=0)
    
    @property
    def display_name(self):
        if self.is_user_root is True:
            return self.owner.get_full_name()
        else:
            return self.name
    
    @property
    def owner(self):
        return self.created_by
    
    @property
    def is_root(self):
        return self.name=='root' and self.parent is None
    
    @property
    def is_user_root(self):
        
        return self.parent_id==1
    
    @models.permalink
    def get_absolute_uri(self):
        return 'album_view', None, {'pk': self.pk}
    
    def save(self, *args, **kwargs):
        created = False
        if self._state.adding:
            created = True
        
        super(Album, self).save(*args, **kwargs)
        if created:
            self.consolidate_count()
        
    def consolidate_count(self):
        from medias.models.image import Image
        self.album_count = self.get_descendant_count()
        self.images_count = Image.objects.filter(album__in=self.get_descendants(include_self=True)).count()
        self.save()
        if self.parent is not None:
            self.parent.consolidate_count()
        
        
    def __unicode__(self):
        if self.is_user_root:
            return self.owner.get_full_name()
        else:
            return self.name

#Post signal to autocreate profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def create_user_root_album(sender, instance, created, **kwargs):
    if created:
        root, created =  Album.objects.get_or_create(name='root',parent=None)
        Album.objects.create(name=instance.pk ,created_by=instance, modified_by=instance, parent=root)

post_save.connect(create_user_root_album, sender=User)    
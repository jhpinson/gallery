from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=512, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    @models.permalink
    def get_absolute_uri(self):
        return 'category_view', None, {'pk': self.pk}
    
    def __unicode__(self):
        return self.name
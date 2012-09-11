from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from django.db import models
from middleware.request import get_current_user

class ChangeTrackMixin(models.Model):
    created_at = AutoCreatedField('created')
    modified_at = AutoLastModifiedField('modified')
    
    created_by = models.ForeignKey("auth.User", default=get_current_user, related_name="create_by_%(class)s_set", editable=False)
    modified_by = models.ForeignKey("auth.User", default=get_current_user, related_name="update_by_%(class)s_set", editable=False)
    
    
    class Meta:
        abstract = True
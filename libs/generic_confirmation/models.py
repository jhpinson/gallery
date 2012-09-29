import datetime
from django.db import models
from django.db.models.query import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from generic_confirmation.fields import PickledObjectField
import hashlib


class ConfirmationManager(models.Manager):
    def confirm(self, token):
        try:
            action = self.exclude(confirmed=True).get(token=token)
        except self.model.DoesNotExist:
            return False
            
        if not action.is_expired():
            action.confirmed = True
            action.save() # FIXME: should we delete() here?
            return action
        
        return False
        
    def resume_form_save(self, token):
        
        action = self.confirm(token)
        if action is not False:
            obj = action.resume_form_save()
            action.delete()
            return obj
        return False
        
    def pending_for(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        now = datetime.datetime.now()
        return self.exclude(confirmed=True).filter(content_type=ct, 
                object_pk=instance.pk).filter(
                Q(valid_until__gt=now) | Q(valid_until__isnull=True)).count()


class DeferredAction(models.Model):
    token = models.CharField(max_length=40)
    valid_until = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False)
    
    form_class = models.CharField(max_length=255)
    form_input = PickledObjectField(editable=False)
    
    content_type = models.ForeignKey(ContentType, null=True)
    object_pk = models.TextField(null=True)
    instance_object = generic.GenericForeignKey('content_type', 'object_pk')
    
    hash = models.CharField(max_length=32, unique=True)
    
    objects = ConfirmationManager()
    
    def save(self, *args, **kwargs):
        
        if self._state.adding:
            md5 = hashlib.md5()
            
            md5.update(str(self.form_input))
            md5.update(str(self.form_class))
            
            if self.object_pk is not None:
                md5.update(str(self.object_pk))
                md5.update("%s.%s" % self.content_type.natural_key())
                
            self.hash = md5.hexdigest()
            
        super(DeferredAction, self).save(*args, **kwargs)
    
    def resume_form_save(self):
        form_class_name = self.form_class
        dot_index = form_class_name.rindex('.')
        module = form_class_name[:dot_index]
        klass = form_class_name[dot_index+1:] 
        form_module = __import__(module, {}, {}, [''])
        form_class = getattr(form_module, klass)
        
        if self.instance_object is None:
            form = form_class(self.form_input)
        else:
            form = form_class(self.form_input, instance=self.instance_object)
        
        if not form.is_valid():
            raise Exception("the defered form was not cleaned properly before saving")
    
        obj = form.save_original()
        obj.save()
        return obj
    
    
    def is_expired(self):
        if self.valid_until is None:
            return False
        now = datetime.datetime.now()
        return self.valid_until < now
    is_expired.boolean = True

    

        
        
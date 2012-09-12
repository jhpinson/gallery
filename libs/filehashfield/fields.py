from django.db.models.fields.files import  FileDescriptor, FileField, FieldFile
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import hashlib



class FileHashFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for ImageHashField. The only difference is
    assigning the hash to the hash_field, if appropriate.
    """
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super(FileHashFileDescriptor, self).__set__(instance, value)

        # To prevent recalculating image hash when we are instantiating
        # an object from the database (bug #11084), only update hash if
        # the field had a value before this assignment.  Since the default
        # value for FileField subclasses is an instance of field.attr_class,
        # previous_file will only be None when we are called from
        # Model.__init__().  The ImageHashField.update_hash_field method
        # hooked up to the post_init signal handles the Model.__init__() cases.
        # Assignment happening outside of Model.__init__() will trigger the
        # update right here.
        if previous_file is not None:
            self.field.update_hash_field(instance, force=True)
            
class FileHashField(FileField):
    attr_class = FieldFile
    descriptor_class = FileHashFileDescriptor
    description = _("Image")
    
    def __init__(self, verbose_name=None, name=None, hash_field='hash', **kwargs):
        self.hash_field = hash_field
        super(FileHashField, self).__init__(verbose_name, name, **kwargs)
    
    def contribute_to_class(self, cls, name):
        super(FileHashField, self).contribute_to_class(cls, name)
        # Attach update_dimension_fields so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        signals.post_init.connect(self.update_hash_field, sender=cls)
        
    def update_hash_field(self, instance, force=False, *args, **kwargs):
        """
        Updates hash field, if defined.

        This method is hooked up to model's post_init signal to update
        hash after instantiating a model instance.  However, hash
        won't be updated if the dimensions fields are already populated.  This
        avoids unnecessary recalculation when loading an object from the
        database.

        Dimensions can be forced to update with force=True, which is how
        ImageFileDescriptor.__set__ calls this method.
        """
        # Nothing to update if the field doesn't have have dimension fields.
        if not self.hash_field:
            return

        # getattr will call the ImageFileDescriptor's __get__ method, which
        # coerces the assigned value into an instance of self.attr_class
        # (ImageFieldFile in this case).
        file = getattr(instance, self.attname)

        # Nothing to update if we have no file and not being forced to update.
        if not file and not force:
            return

        hash_field_filled = not(
            (self.hash_field and not getattr(instance, self.hash_field))
        )
        # When both dimension fields have values, we are most likely loading
        # data from the database or updating an image field that already had
        # an image stored.  In the first case, we don't want to update the
        # dimension fields because we are already getting their values from the
        # database.  In the second case, we do want to update the dimensions
        # fields and will skip this return because force will be True since we
        # were called from ImageFileDescriptor.__set__.
        if hash_field_filled and not force:
            return

        # file should be an instance of ImageFieldFile or should be None.
        if file:
            md5 = hashlib.md5()
            file.open()
            for chunk in file.chunks():
                md5.update(chunk)
            hash = md5.hexdigest()
        else:
            # No file, so clear hash field.
            hash = None

        # Update the width and height fields.
        if self.hash_field:
            setattr(instance, self.hash_field, hash)


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^filehashfield\.fields\.FileHashField"])

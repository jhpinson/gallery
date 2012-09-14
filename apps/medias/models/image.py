from django.db import models
from .media import Media, Thumbnail
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from sorl.thumbnail import delete
from django.conf import settings
from imagehashfield.fields import ImageHashField

class Image(Media):
    
    def upload_path(self, filename):
        return '%s/%s' % ('/'.join([c.name for c in self.album.get_ancestors()] + [self.album.name]), filename)
    
    #file = ImageHashField(upload_to=upload_path, height_field='height', width_field='width', hash_field='hash', max_length=1024)
    
    #width = models.PositiveIntegerField()
    #height = models.PositiveIntegerField()
    
    def generate_thumbnail(self, size):
        image = get_thumbnail(self.file.file, "%sx%s" % (settings.THUMBNAIL_SIZES[size]['width'], settings.THUMBNAIL_SIZES[size]['height']), upscale=True)
        
        data = {'url' : image.url, 'width':image.width, 'height':image.height}
        
        thumb = Thumbnail(media=self, size=size, **data)
        thumb.save()
        
        return data
        
    def delete(self, *args, **kwargs):
        
        delete(self.file.file)
        self.file.delete(save=False)
        
        super(Image, self).delete(*args, **kwargs)
        
        
    class Meta:
        app_label = 'medias'
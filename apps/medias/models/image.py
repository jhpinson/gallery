from django.db import models
from .media import Media, Thumbnail
from sorl.thumbnail.fields import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from sorl.thumbnail import delete
from django.conf import settings

class Image(Media):
    
    def upload_path(self, filename):
        return '%s/%s' % ('/'.join([c.name for c in self.category.get_ancestors()] + [self.category.name]), filename)
    
    file = ImageField(upload_to=upload_path)
    
    def generate_thumbnail(self, size):
        image = get_thumbnail(self.file.file, str(settings.THUMBNAIL_SIZES[size]['width']), upscale=True)
        
        data = {'url' : image.url, 'width':image.width, 'height':image.height}
        
        thumb = Thumbnail(media=self, **data)
        thumb.save()
        
        return data
        
    def delete(self, *args, **kwargs):
        
        self.file.delete_file()
        delete(self.file.file)
        super(Image, self).delete(*args, **kwargs)
        
        
    class Meta:
        app_label = 'medias'
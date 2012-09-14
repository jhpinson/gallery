from .media import Media, Thumbnail
from sorl.thumbnail.shortcuts import get_thumbnail
from sorl.thumbnail import delete
from django.conf import settings

class Image(Media):
    
    def upload_path(self, filename):
        return '%s/%s' % ('/'.join([c.name for c in self.album.get_ancestors()] + [self.album.name]), filename)
    
    
    
    def generate_thumbnails(self):
        self.generate_thumbnail('small')
        self.generate_thumbnail('medium')
        self.generate_thumbnail('large')
    
    def generate_thumbnail(self, size):
        image = get_thumbnail(self.file.file, "%sx%s" % (settings.THUMBNAIL_SIZES[size]['width'], settings.THUMBNAIL_SIZES[size]['height']), upscale=True)
        
        data = {'url' : image.url, 'width':image.width, 'height':image.height}
        
        thumb = Thumbnail(media=self, size=size, **data)
        thumb.save()
        
        return data
        
    def delete(self, *args, **kwargs):
        
        try:
            delete(self.file.file)
        except IOError:
            pass
        self.file.delete(save=False)
        
        super(Image, self).delete(*args, **kwargs)
        
        
    class Meta:
        app_label = 'medias'
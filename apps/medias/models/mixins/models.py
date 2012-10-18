from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

class ThumbAccessors(object):
    
    def __init__(self, *args, **kwargs):
        self._cache = {}
        super(ThumbAccessors, self).__init__(*args, **kwargs)
    
    def thumbnail_small(self):
        return self.__generic_thumb_accessor('thumbnail_small')
    
    def thumbnail_medium(self):
        return self.__generic_thumb_accessor('thumbnail_medium')
    
    def thumbnail_large(self):
        return self.__generic_thumb_accessor('thumbnail_large')
    
    
    
    
    def __generic_thumb_accessor(self, name):
    
        if name[:10] == 'thumbnail_' or name[:10] == 'lazythumb_':
            
            if self._cache.get(name, None) is None:
            
                size = name[10:]
                data = {'pk' : self.pk}
                try:
                    thumb = self.thumbnails.get(size=size)
                    data['url'] = thumb.url
                    data['width'] = thumb.width
                    data['height'] = thumb.height
                    data['exists'] = True
                    
                    self._cache[name] = data
                except ObjectDoesNotExist:
                    data['url'] = reverse('lazy_thumbnail_view', kwargs={'pk' : self.pk, 'size' : size})
                    data['width'] = settings.THUMBNAIL_SIZES[size]['width']
                    data['height'] = settings.THUMBNAIL_SIZES[size]['height']
                    data['exists'] = True
                    self._cache[name] = data
            
            return self._cache[name]
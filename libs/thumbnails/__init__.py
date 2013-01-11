from sorl.thumbnail.base import ThumbnailBackend , EXTENSIONS
from sorl.thumbnail.helpers import tokey, serialize
from sorl.thumbnail.conf import settings
import uuid

class CustomThumbnailBackend(ThumbnailBackend):
    
    def _get_thumbnail_filename(self, source, geometry_string, options):
        """
        Computes the destination filename.
        """
        key = tokey(source.key, geometry_string, serialize(options), uuid.uuid4())
        # make some subdirs
        path = '%s/%s/%s' % (key[:2], key[2:4], key)
        return '%s%s.%s' % (settings.THUMBNAIL_PREFIX, path,
                            EXTENSIONS[options['format']])
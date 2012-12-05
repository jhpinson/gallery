from .media import Media, Thumbnail
from .image import Image
from .videos import Video, VideoVersion
from .album import Album
from django.core.files.base import ContentFile

__all__ = ['Media', 'Image', 'Thumbnail', 'Video', 'VideoVersion', 'Album', 'create_media']


import uuid

def create_media(album, f, filename, created_at):
    
    filename = filename.lower()
    file_ext = filename.split('.')[-1]
    
    if file_ext in ['mpg', 'avi', 'mov', 'mts']:
        media = Video()
    else:
        media = Image()
        
    media.name = filename
    media.parent_album = album
    media.file_creation_date = created_at
    media.original_file.save(
                      '%s.%s' % (uuid.uuid4(), file_ext)
                      , ContentFile(f.read()), save=False)
    
    
    media.save()
    media.generate_thumbnails()
    
    return media
        
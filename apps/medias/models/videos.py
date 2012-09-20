from medias.models.media import Media
from django.db import models
from model_utils import Choices
from helpers.ffmpeg import webm

class Video(Media):
    
    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
        #self.generate_versions()
        
    def generate_versions(self):
        
        #if not self.video_versions.filter(type=VideoVersion.TYPES.webm).exists():
        return webm(self.file.path)
            
            
        
    class Meta:
        app_label = 'medias'
        
        
class VideoVersion(models.Model):
    
    TYPES = Choices(('webm', 'video/webm'),)
    
    video = models.ForeignKey(Video, related_name='video_versions')
    file = models.FileField(upload_to='videos-versions/%Y/%m/',  max_length=1024, null=False)
    type = models.CharField(max_length=10, choices=TYPES, null=False)
    
    class Meta:
        app_label = 'medias'
from medias.models.media import Media
from django.db import models
from model_utils import Choices
from helpers.ffmpeg import webm, thumbnail
from django.core.files.base import ContentFile
import os

class Video(Media):
    
    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
        #self.generate_versions()
        
    def generate_thumbnails(self):
        
        retcode, stdtout, stderr, tmp_file = thumbnail(self.file.path)
        
        if retcode == 0:
            
            f = open(tmp_file, 'r')
            
            self.generate_thumbnail('small', f)
            f.seek(0)
            self.generate_thumbnail('medium', f)
            f.seek(0)
            self.generate_thumbnail('large', f)
        
    def generate_versions(self):
        
        if not self.video_versions.filter(type=VideoVersion.TYPES.webm).exists():
            try:
                retcode, stdtout, stderr, tmp_file = webm(self.file.path)
            except Exception:
                retcode = 1
            
            version = VideoVersion(video=self, type=VideoVersion.TYPES.webm)
            
            if retcode == 0:
                version.status = VideoVersion.STATUSES.ready
                f = open(tmp_file, 'r')
                version.file.save("%s.webm" % self.pk, ContentFile(f.read()), save=False)
                f.close()
                os.remove(tmp_file)
            else:
                version.status = VideoVersion.STATUSES.failed
            version.save()
                
    class Meta:
        app_label = 'medias'
        
        
class VideoVersion(models.Model):
    
    TYPES = Choices(('webm', 'video/webm'),)
    STATUSES = Choices('ready', 'failed')
    
    video = models.ForeignKey(Video, related_name='video_versions')
    file = models.FileField(upload_to='videos-versions/%Y/%m/',  max_length=1024, null=False)
    type = models.CharField(max_length=10, choices=TYPES, null=True)
    
    status = models.CharField(max_length=50, choices=STATUSES)
    
    class Meta:
        app_label = 'medias'
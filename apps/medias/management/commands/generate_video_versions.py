from django.core.management.base import BaseCommand
from medias.models import Video
from helpers.ffmpeg import metadata
from medias.models.videos import VideoVersion
from time import sleep

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        while True:
            for video in Video.objects.filter(video_status=Video.VIDEO_STATUSES.pending).iterator():
                video.generate_versions()
                
                if video.video_versions.filter(status=VideoVersion.STATUSES.ready).count() > 0:
                    
                    video.video_status = Video.VIDEO_STATUSES.done
                    
                elif video.video_versions.all().count() > 0:
                    
                    video.video_status = Video.VIDEO_STATUSES.failed
                
                video.save()
                
                print "done %s" % video.pk
        
        sleep(5)
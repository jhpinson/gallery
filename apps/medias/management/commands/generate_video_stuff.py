from django.core.management.base import BaseCommand
from medias.models import Video
from helpers.ffmpeg import metadata

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        for video in Video.objects.all():
            try:
                video_date = metadata(video.file.path)
                if video_date is not None:
                    video.date = video_date 
                video.generate_versions()
                video.generate_thumbnails()
                print "done %s" % video.pk
            except Exception,e:
                print "ERROR %s" % e
                print e.__class__
        
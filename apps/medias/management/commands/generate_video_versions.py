from django.core.management.base import BaseCommand
from medias.models import Video
from helpers.ffmpeg import metadata

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        for video in Video.objects.all():
                video.video_versions.all().delete()
                video.thumbnails.all().delete()
                meta = metadata(video.file.path)
                video_date = meta.get('date')
                if video_date is not None:
                    video.date = video_date 
                video.generate_versions()
                video.generate_thumbnails()
                print "done %s" % video.pk
        
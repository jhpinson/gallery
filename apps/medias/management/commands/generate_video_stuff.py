from django.core.management.base import BaseCommand
from medias.models import Video

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        for video in Video.objects.all():
            try:
                video.generate_versions()
                print "done %s" % video.pk
            except Exception,e:
                print "ERROR %s" % e
                print e.__class__
        
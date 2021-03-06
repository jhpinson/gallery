from django.core.management.base import BaseCommand
from medias.models import Image

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        self.generate('small')
        #self.generate('small')
        self.generate('large')
        
    def generate(self, size):
        
        images = Image.objects.all().exclude(thumbnails__size=size)
        i = 0
        total = images.count()
        for image in images:
            i += 1
            try:
                image.generate_thumbnail(size)
                
            except IOError,e:
                print "IOERROR deleting file", image.pk, image.file.url, image.delete()
                
            except Exception,e:
                print e, image.pk, image.file.url
        
            print "%s %s / %s" % (size, i, total)
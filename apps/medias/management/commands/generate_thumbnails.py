from django.core.management.base import BaseCommand
from medias.models import Image

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        self.generate('small')
        #self.generate('small')
        #self.generate('large')
        
    def generate(self, size):
        
        images = Image.objects.all()
        i = 0
        total = images.count()
        for image in images:
            i += 1
            try:
                image.url_small = None
                image.generate_thumbnail(size)
                image.save()
            except IOError,e:
                print "IOERROR deleting file", image.pk, image.file.url
                
                
            except Exception,e:
                print e, image.pk, image.file.url
            print "%s %s / %s" % (size, i, total), image.pk

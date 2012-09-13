from django.core.management.base import BaseCommand
from medias.models import Image

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        images = Image.objects.all()
        i = 0
        total = images.count()
        for image in images.order_by('pk'):
            i += 1
            try:
                image.generate_thumbnail('small')
            except Exception,e:
                pass
            
            try:
                image.generate_thumbnail('medium')
            except Exception,e:
                pass
            
            try:
                image.generate_thumbnail('large')
            except Exception,e:
                pass
            
            print '%s / %s' % (i, total)
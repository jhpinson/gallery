from django.core.management.base import BaseCommand
from medias.models import Media

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        for media in Media.objects.all():
            print media.pk
            media.cast().save()
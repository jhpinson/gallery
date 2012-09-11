from django.core.management.base import BaseCommand
from structures.models import Album

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        Album.objects.create(name='root', parent=None, created_by_id=1, modified_by_id=1)
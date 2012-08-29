from django.views.generic.base import View
from django.http import HttpResponse
from medias.models import Media
from django.utils import simplejson

class GenerateThumbnail(View):
    
    def get(self, request, *args, **kwargs):
        m = Media.objects.get(pk=kwargs.get('pk'))
        
        json = m.cast().generate_thumbnail(kwargs.get('size'))
        
        return HttpResponse(simplejson.dumps(json), content_type='application/json')
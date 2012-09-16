from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required




class GenerateThumbnail(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateThumbnail, self).dispatch( request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        from medias.models.media import Media
        m = Media.objects.get(pk=kwargs.get('pk'))
        json = m.cast().generate_thumbnail(kwargs.get('size'))
        return HttpResponse(simplejson.dumps(json), content_type='application/json')
    
    

class LazyThumbnail(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LazyThumbnail, self).dispatch( request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        from medias.models.media import Thumbnail
        from medias.models.media import Media
        m = Media.objects.get(pk=kwargs.get('pk'))
        size = kwargs.get('size')
        
        try:
            url = Thumbnail.objects.get(media=m, size=size).url
        except ObjectDoesNotExist:
            url = m.cast().generate_thumbnail(kwargs.get('size'))['url']
        
        return HttpResponseRedirect(url)
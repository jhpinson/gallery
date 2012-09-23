from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from ..models import Media, Image, Video

class ModalVideoView(DetailView):
    model = Video
    template_name = 'medias/modal-video-player.html'

class MediaView(DetailView):
    model = Media
    queryset = Media.objects.models(Image, Video).select_subclasses()
    template_name = 'medias/media_detailview.html'
    
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
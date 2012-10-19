from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect

from django.utils import simplejson

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from ..models import Media, Image, Video, Thumbnail
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

class ModalVideoView(DetailView):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ModalVideoView, self).dispatch( request, *args, **kwargs)
    
    model = Video
    template_name = 'medias/modal-video-player.html'

    
class MediaView(DetailView):
    model = Media
    
    def get(self, request, *args, **kwargs):
        
        media = self.get_object()
        position = media.get_position() + 1
        
        return HttpResponseRedirect("%s?page=%s" % (reverse('album_media_view', kwargs={'pk': media.parent_album.pk}), position))
    
class AlbumMediaView(ListView):
    model = Media
    
    template_name = 'medias/media_detailview.html'
    paginate_by = 1
    context_object_name = 'object'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumMediaView, self).dispatch( request, *args, **kwargs)
    
    def get_queryset(self):
        return Media.objects.models(Image, Video).filter(parent_album_id=self.kwargs.get('pk')).select_subclasses()
    
    def get_context_data(self, **kwargs):
        context = super(AlbumMediaView, self).get_context_data(**kwargs)
        context['object'] = context['object'][0] 
                
        context['breadcrumbs'] =  [ context['object'].parent_album, context['object']]
        
        return context
    
class GenerateThumbnail(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GenerateThumbnail, self).dispatch( request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        m = Media.objects.get(pk=kwargs.get('pk'))
        json = m.cast().generate_thumbnail(kwargs.get('size'))
        return HttpResponse(simplejson.dumps(json), content_type='application/json')
    
    

class LazyThumbnail(View):
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LazyThumbnail, self).dispatch( request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        
        m = Media.objects.get(pk=kwargs.get('pk'))
        size = kwargs.get('size')
        
        try:
            url = Thumbnail.objects.get(media=m, size=size).url
        except ObjectDoesNotExist:
            url = m.cast().generate_thumbnail(kwargs.get('size'))['url']
        
        return HttpResponseRedirect(url)
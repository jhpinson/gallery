# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import utc, get_current_timezone
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.core.files.uploadedfile import UploadedFile
from django.db.utils import IntegrityError
from django.db import connection

from PIL import Image as PILImage
from PIL.ExifTags import TAGS

from dateutil.parser import parse
import datetime

from ..forms import AlbumForm
from ..models import Album, Video, Image, Media

from django.core.exceptions import ObjectDoesNotExist
from middleware.request import get_current_user
from django.contrib.contenttypes.models import ContentType
from urlparse import urlparse, parse_qs
from django.utils.http import urlencode
from helpers.ffmpeg import metadata

MONTH = ['Janvier', u'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', u'Août', 'Septembre', 'Octobre', 'novembre', u'Décembre']

def construct_url(url, query_dict = None, clean=False):
    parse_result = urlparse(url)
    
    query = {}
    if not clean:
        if len(parse_result.query) > 0:
            query = parse_qs(parse_result.query)
            
            for key, value in query.iteritems():
                query[key] = value
      
    
    if query_dict is not None:
        for key, value in query_dict.iteritems():
            query[key] = [value]
            
    if len(query.keys()) > 0:
        _query= []
        for key, values in query.iteritems():
            if len(values) == 1:
                _query.append(urlencode({key: values[0]}))
            else:
                for value in values:
                    _query.append(urlencode({key: value}))
                
        query = '&'.join(_query)
    else:
        query = None
        
    return "%s%s%s" % ( parse_result.path, "?%s" % query if query is not None else '', "#%s" % parse_result.fragment if len(parse_result.fragment) > 0 else '')

class AlbumView(ListView):
    
    template_name = 'albums/album.html'
    paginate_by = 25
    _album = None
    
    
    @csrf_exempt
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumView, self).dispatch( request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        name = filename.lower()
        
        if filename.lower().split('.')[-1] in ['mpg', 'avi', 'mov', 'mts']:
            
            new_video = Video()
            new_video.name = name
            new_video.parent_album=self.get_album()
            new_video.date= parse(request.POST.get(filename)).replace(tzinfo=utc).astimezone(get_current_timezone()).replace(tzinfo=None)
            new_video.file.save(
                              filename
                              , file, save=True)
            
            video_date = metadata(new_video.file.path)
            if video_date is not None:
                new_video.date = video_date
                new_video.save()
            
            new_video.generate_thumbnails()
            
        else:
        
            img = PILImage.open(file)
            
            try:
                
                new_image = Image()
                exif = img._getexif()
                if exif is not None:
                    for tag, value in exif.items():
                        decoded = TAGS.get(tag, tag)
                        if  decoded == 'DateTimeOriginal':
                            new_image.date = datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                            break
                
                    
                
                new_image.name = name
                new_image.parent_album=self.get_album()
                
                if new_image.date is None:
                    new_image.date= parse(request.POST.get(filename)).replace(tzinfo=utc).astimezone(get_current_timezone()).replace(tzinfo=None)
                
                new_image.file.save(
                              filename
                              , file, save=True)
                
                new_image.generate_thumbnails()
                
            except IntegrityError,e:
                print e
                return HttpResponseServerError(u"Le fichier \"%s\" est déja présent dans cet album" % filename) 
        
        
        return HttpResponse(simplejson.dumps({'name' : request.FILES.items()[0][1].name}), content_type="application/json")
    
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        if self.request.GET.get('thumbnails') is not None:
            
            template = 'albums/_inc/thumbnails.html'
        else:
            template = self.get_template_names()
            
        return self.response_class(
                request = self.request,
                template = template,
                context = context,
                **response_kwargs
            )
    
    def get_album(self):
        
        if self._album is None:
        
            pk = self.kwargs.get('pk', None)
            
            if pk is not None:
                self._album = Album.objects.get(pk=pk)
            else:
                try:
                    self._album = Album.objects.get(parent_album__name='root', parent_album__parent_album=None)
                except ObjectDoesNotExist:
                    root, created =  Album.objects.get_or_create(name='root',parent_album=None)
                    self._album = Album.objects.create(name=get_current_user().pk , parent_album=root)
        
        return self._album
        
    def get_queryset(self):
        filters = {}
        
        if self.get_album().is_leaf:
            qs = self.get_album().medias.models(Image, Video).select_subclasses().order_by('date')
        else:
            qs = self.get_album().medias.models(Album).select_subclasses().order_by('-date')
        
        for facet, value in self.get_current_facets().iteritems():
             
            if facet in ['year', 'month']:
                filters['date__%s' % facet] = value
        
        if len(filters.keys()) > 0:
            qs = qs.filter(**filters)
            
        return qs.select_subclasses()

        
        
    
    def get_current_facets(self):
        
        facets = {}
        if self.request.GET.get('year', None) is not None:
            facets['year'] = self.request.GET.get('year')
             
        if self.request.GET.get('month', None) is not None and facets.get('year', None) is not None:
            facets['month'] = self.request.GET.get('month')

        return facets
    
    
    def get_context_data(self, **kwargs):
        
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['album'] = self.get_album()
        
        # get facets
        current_facets = self.get_current_facets()
        facets = {}
        url = self.request.get_full_path()
        
        cursor = connection.cursor()
        #cursor.execute("SELECT real_type_id, count(*) from medias_media where parent_album_id=%s group by real_type_id", [self.get_album().pk])
        #facets['real_type'] = []
        #for res in cursor.fetchall():
        #    facets['real_type'].append({'name' :ContentType.objects.get(pk=res[0]).model, 'count' : res[1], 'url' : None})
        
        if self.get_album().is_leaf:
            real_types = [ContentType.objects.get_for_model(Image).pk, ContentType.objects.get_for_model(Video).pk,]
        else:
            real_types = [ContentType.objects.get_for_model(Album).pk] * 2
        
        
        cursor.execute("SELECT year(date), count(*) from medias_media where parent_album_id=%s and real_type_id in %s group by  year(date)", [self.get_album().pk, real_types])
        facets['year'] = []
        for res in cursor.fetchall():
            if  current_facets.get('year') is not None and int(current_facets.get('year')) == int(res[0]):
                continue
            facets['year'].append({'name' :res[0], 'nb' : res[1], 'url' : construct_url(url, {'year' : res[0]}, clean=True)})
        
        if current_facets.get('year') is not None:
                
            cursor.execute("SELECT month(date), count(*) from medias_media where year(date) = %s and parent_album_id=%s and real_type_id in %s group by  month(date)", [current_facets.get('year'), self.get_album().pk, real_types])
            facets['month'] = []
            for res in cursor.fetchall():
                if current_facets.get('month') is not None and int(current_facets.get('month')) == int(res[0]):
                    continue
                facets['month'].append({'name' :MONTH[res[0]-1]   , 'nb' : res[1], 'url' : construct_url(url, {'month' : res[0], 'year' : current_facets.get('year')}, clean=True)})
            
        if current_facets.get('year') is not None:
            current_facets['year'] = {'name' : current_facets['year'], 'url' : construct_url(url, clean=True)}
            
        if current_facets.get('month') is not None:
            current_facets['month'] = {'name' : MONTH[int(current_facets['month'])-1], 'url' : construct_url(url, {'year' : current_facets.get('year')}, clean=True)}
            
        context['facets'] = facets
        context['current_facets'] = current_facets
        # root album
        if self.get_album().parent_album is not None:
            context['breadcrumbs'] = self.get_album().get_ancestors()[1:] + [self.get_album()]
            
        return context
    
    
class GalleryView(TemplateView):
    
    template_name = 'gallery/gallery.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GalleryView, self).dispatch( request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        
        context['medias'] = Album.objects.get(pk=kwargs.get('pk')).medias.models(Image, Video).select_subclasses()
        
        return context
   
class UpdateAlbum(UpdateView):
    template_name = 'albums/create_or_edit.html'
    model = Album
    form_class = AlbumForm
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateAlbum, self).dispatch( request, *args, **kwargs)
    
class CreateAlbum(CreateView):
    template_name = 'albums/create_or_edit.html'
    model = Album
    form_class = AlbumForm
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateAlbum, self).dispatch( request, *args, **kwargs)
    
    def get_form_kwargs(self):
        
        data = super(CreateAlbum, self).get_form_kwargs()
        
        data['initial']['parent_album'] = self.kwargs.get('pk')
        return data
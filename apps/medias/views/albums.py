# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView, View
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
from django.utils.dateformat import format


from dateutil.parser import parse
import datetime

from ..forms import AlbumForm
from ..models import Album, Video, Image, create_media

from django.contrib.contenttypes.models import ContentType
from urlparse import urlparse, parse_qs
from django.utils.http import urlencode
from helpers.ffmpeg import metadata
from django.contrib.auth.models import User
from ..forms import MoveForm

#MONTH = ['Janvier', u'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', u'Août', 'Septembre', 'Octobre', 'novembre', u'Décembre']

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
            if value is not None:
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

class SearchAlbum(View):
    
    def get(self, request, *args, **kwargs):
        res = []
        query = request.GET.get('q')
        for a in Album.objects.filter(name__istartswith=query):
            res.append({'value' : a.pk, 'label' : a.name})
        
        return HttpResponse(simplejson.dumps(res), content_type='application/json')
    
class AlbumView(ListView):
    
    template_name = 'albums/album.html'
    paginate_by = 25
    _album = None
    
    
    @csrf_exempt
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumView, self).dispatch( request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        
        f = request.FILES[u'files[]']
        wrapped_file = UploadedFile(f)
        
        try:
            create_media(self.get_album(), f, wrapped_file.name, parse(request.POST.get(wrapped_file.name)).replace(tzinfo=utc).astimezone(get_current_timezone()).replace(tzinfo=None))
        except IntegrityError,e:
            print e
            return HttpResponseServerError(u"Le fichier \"%s\" est déja présent dans cet album" % wrapped_file.name) 
        
        
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
                self._album = False
                
            """else:
                try:
                    self._album = Album.objects.get(parent_album__name='root', parent_album__parent_album=None)
                except ObjectDoesNotExist:
                    root, created =  Album.objects.get_or_create(name='root',parent_album=None)
                    self._album = Album.objects.create(name=get_current_user().pk , parent_album=root)
            """
            
        return self._album
        
    def get_queryset(self):
        filters = {}
        
        if self.get_album():
            qs = self.get_album().medias.models(Image, Video).select_subclasses().order_by('date').select_subclasses()
        else:
            qs = Album.objects.all().order_by('-date')
        for facet, value in self.get_current_facets().iteritems():
             
            if facet in ['year', 'month', 'day']:
                filters['date__%s' % facet] = value
            
            if facet == 'type':
                filters['real_type_id'] = value
                
            if facet == 'user':
                filters['created_by_id'] = value
                
        if len(filters.keys()) > 0:
            qs = qs.filter(**filters)
            
        return qs

        
    
    def get_current_facets(self):
        
        facets = {}
        if self.request.GET.get('year', None) is not None:
            facets['year'] = self.request.GET.get('year')
            
        if self.request.GET.get('user', None) is not None:
            facets['user'] = self.request.GET.get('user')
             
        if self.request.GET.get('month', None) is not None:
            facets['month'] = self.request.GET.get('month')
            
        if self.request.GET.get('day', None) is not None:
            facets['day'] = self.request.GET.get('day')
            
        if self.request.GET.get('type', None) is not None:
            facets['type'] = self.request.GET.get('type')
        
        return facets
    
    def get_day(self, year, month, day):
        return "%s %s" %( format(datetime.date(int(year), int(month) ,int(day)), 'l' ), day)
    
    def get_month(self, year, month):
        return format(datetime.date(int(year), int(month), 1), 'F')
        
    def get_type(self, ct):
        return ContentType.objects.get(pk=ct).model_class()._meta.verbose_name
    
    def get_user(self, id):
        
        return User.objects.get(pk=id).get_full_name()
    
    def get_context_data(self, **kwargs):
        
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['album'] = self.get_album()
        
        # get facets
        current_facets = self.get_current_facets()
        facets = {}
        url = self.request.get_full_path()
        
        context['move_form'] = MoveForm
        
        cursor = connection.cursor()
        #cursor.execute("SELECT real_type_id, count(*) from medias_media where parent_album_id=%s group by real_type_id", [self.get_album().pk])
        #facets['real_type'] = []
        #for res in cursor.fetchall():
        #    facets['real_type'].append({'name' :ContentType.objects.get(pk=res[0]).model, 'count' : res[1], 'url' : None})
                
        
        full_qs_pk =  [v[0] for v in context['page_obj'].paginator.object_list.values_list('pk')]
        if len(full_qs_pk) == 1:
            full_qs_pk = full_qs_pk * 2
        
        if len(full_qs_pk) > 1:
            
            cursor.execute("SELECT real_type_id, count(*) from medias_media where  id in %s  group by real_type_id", [full_qs_pk])
            facets['type'] = []
            for res in cursor.fetchall():
                if current_facets.get('type') is not None and int(current_facets.get('type')) == int(res[0]):
                    continue
                facets['type'].append({'name' :self.get_type(res[0]), 'nb' : res[1], 'value' : res[0], 'param' : 'type'})
           
            cursor.execute("SELECT created_by_id, count(*) from medias_media where  id in %s  group by created_by_id", [full_qs_pk])
            facets['user'] = []
            for res in cursor.fetchall():
                if current_facets.get('user') is not None and int(current_facets.get('user')) == int(res[0]):
                    continue
                facets['user'].append({'name' :self.get_user(res[0]), 'nb' : res[1], 'value' : res[0], 'param' : 'user'})
           
            
            
            cursor.execute("SELECT year(date), count(*) from medias_media where id in %s group by  year(date)", [full_qs_pk])
            facets['year'] = []
            for res in cursor.fetchall():
                facets['year'].append({'name' :res[0], 'nb' : res[1], 'value' : res[0], 'param' : 'year'})
                
                if current_facets.get('year') is not None and int(current_facets.get('year')) == int(res[0]):
                        facets['year'][-1]['current'] = True
                
            # si  facet year => month or day ?
            if current_facets.get('year') is not None or len(facets['year']) == 1:
                
                year = current_facets.get('year', facets['year'][0]['value'])
                    
                cursor.execute("SELECT month(date), count(*) from medias_media where  id in %s group by  month(date)", [ full_qs_pk])
                facets['month'] = []
                for res in cursor.fetchall():
                    
                    facets['month'].append({'name' :self.get_month(year, res[0])   , 'nb' : res[1], 'value' : res[0], 'param' : 'month'})
                    
                    if current_facets.get('month') is not None and int(current_facets.get('month')) == int(res[0]):
                        facets['month'][-1]['current'] = True
                  
                if current_facets.get('month') is not None or len(facets['month']) == 1:
                    month =  current_facets.get('month', facets['month'][0]['value'])
                    cursor.execute("SELECT day(date), count(*) from medias_media where  id in %s  group by  day(date)", [full_qs_pk])
                    facets['day'] = []
                    for res in cursor.fetchall():
                        
                        if current_facets.get('day') is not None and int(current_facets.get('day')) == int(res[0]):
                            continue
                        facets['day'].append({'name' : self.get_day(year, month, res[0])   , 'nb' : res[1], 'value' : res[0], 'param' : 'day'})
            
           
        if current_facets.get('month') is None and len(facets.get('month', []))>1:
            try:
                del  facets['day']
            except KeyError:
                pass
                
            
        
        current_facets_value = dict(current_facets)
        
        context['current_facets'] = []
        
        if current_facets.get('user') is not None:
            context['current_facets'].append({'name' : self.get_user(current_facets['user']), 'value' : current_facets['user'], 'url' : construct_url(url, dict(current_facets_value, user=None),clean=True)})
        
        if current_facets.get('type') is not None:
            context['current_facets'].append({'name' : self.get_type(current_facets['type']), 'value' : current_facets['type'], 'url' : construct_url(url, dict(current_facets_value, type=None),clean=True)})
        
        if current_facets.get('year') is not None:
            context['current_facets'].append({'name' : current_facets['year'], 'value' : current_facets['year'], 'url' : construct_url(url, dict(current_facets_value, year=None, month=None, day=None), clean=True)})
            
        if current_facets.get('month') is not None:
            context['current_facets'].append({'name' : self.get_month(year, current_facets.get('month')), 'value' : current_facets['month'], 'url' : construct_url(url, dict(current_facets_value,  month=None, day=None), clean=True)})
            
        if current_facets.get('day') is not None:
            context['current_facets'].append({'name' : self.get_day(year, month, current_facets['day']) , 'url' : construct_url(url, dict(current_facets_value, day=None), clean=True)})
            
        for facet in facets.keys():
            
            facets[facet] = [v for v in facets[facet] if v.get('current', False) is not True]
            
            if len(facets[facet]) <= 1:
                facets[facet] = None
            
            
            
        context['facets'] = facets
        # root album
        if self.get_album() :
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
        
        data['initial']['parent_album'] = self.kwargs.get('pk', None)
        return data
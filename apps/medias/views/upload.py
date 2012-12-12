# -*- coding: utf-8 -*-
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from ..models import create_media, Album
from _mysql_exceptions import IntegrityError
from django.http import  HttpResponse
from django.utils import simplejson
from django.utils.timezone import utc, get_current_timezone
from dateutil.parser import parse

class UploadView(View):
    
    
    @csrf_exempt
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UploadView, self).dispatch( request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        
        f = request.FILES[u'files[]']
        wrapped_file = UploadedFile(f)
        
        cid = request.POST.get('cid')
        
        try:
            media = create_media(Album.objects.get(pk=request.POST.get('album')), f, wrapped_file.name, parse(request.POST.get(wrapped_file.name)).replace(tzinfo=utc).astimezone(get_current_timezone()).replace(tzinfo=None))
        except IntegrityError,e:
            print e
            return HttpResponse(simplejson.dumps({'cid' : cid, 'success' : False, 'error' : 'IntegrityError'}), content_type="application/json")
        
        
        return HttpResponse(simplejson.dumps({'cid' : cid, 'id' : media.pk, 'success' : True, 'error' : None}), content_type="application/json")
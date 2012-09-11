from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from structures.views import AlbumView
admin.autodiscover()

urlpatterns = patterns('')

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

try:
    import uwsgi
    urlpatterns += url(r'^uwsgi/', include('uwsgi_admin.urls')),
except ImportError:
    pass



urlpatterns += patterns('',
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
                        
    (r'^$', AlbumView.as_view(), {}, "home_view"),
    # custom auth
    url(r'', include('auth.urls')),
    # albums
    url(r'', include('structures.urls')),
    # medias
    url(r'', include('medias.urls')),
    
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG: 
    if getattr(settings,'DISABLE_ROBOTS',False) is True:
        from django.http import HttpResponse
        urlpatterns += patterns('', 
                        url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
                        )
        
    urlpatterns += patterns('', 
                            url(r'^%s/(?P<path>.*)/?$' % settings.MEDIA_URL[1:-1] , 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT,}),
                            (r'^404$', TemplateView.as_view(template_name="404.html")),
                            (r'^500$', TemplateView.as_view(template_name="500.html")), 
                            )
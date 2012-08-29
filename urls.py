from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from structure.views import CategoryView
admin.autodiscover()

urlpatterns = patterns('')

try:
    import uwsgi
    urlpatterns += url(r'^uwsgi/', include('uwsgi_admin.urls')),
except ImportError:
    pass


urlpatterns += patterns('',
    (r'^$', CategoryView.as_view(), {}, "home_view"),
    url(r'', include('structure.urls')),
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
from django.conf.urls.defaults import patterns, include, url
from medias.views import GenerateThumbnail, LazyThumbnail


urlpatterns = patterns('',
    (r'^thumbnail/generate/(?P<pk>\d+)/(?P<size>.+)/$', GenerateThumbnail.as_view(), {}, "generate_thumbnail_view"),
    (r'^thumbnail/lazy/(?P<pk>\d+)/(?P<size>.+)/$', LazyThumbnail.as_view(), {}, "lazy_thumbnail_view"),
    
)
from django.conf.urls.defaults import patterns, include, url
from medias.views import GenerateThumbnail


urlpatterns = patterns('',
    (r'^thumbnail/generate/(?P<pk>\d+)/(?P<size>.+)/$', GenerateThumbnail.as_view(), {}, "generate_thumbnail_view"),
)
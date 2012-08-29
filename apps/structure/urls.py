from django.conf.urls.defaults import patterns, include, url
from .views import CategoryView


urlpatterns = patterns('',
    (r'^(?P<pk>\d+)/$', CategoryView.as_view(), {}, "category_view"),
    
)
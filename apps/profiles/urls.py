from django.conf.urls.defaults import patterns, include, url
from .views import RestProfileView



urlpatterns = patterns('',
    
    url(RestProfileView.make_url(), RestProfileView.as_view(), name='rest_profile_view'),
             
    
)

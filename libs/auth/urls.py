
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'auth.views.login', name='login'),
    url(r'^popup-login/$', 'auth.views.popup_login', name='popup_login'),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)

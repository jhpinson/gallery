from django.conf.urls.defaults import patterns
from .views import AlbumView
from structures.views import GalleryView, CreateAlbum, UpdateAlbum


urlpatterns = patterns('',
    (r'^(?P<pk>\d+)/$', AlbumView.as_view(), {}, "album_view"),
     (r'^gallery/(?P<pk>\d+)/$', GalleryView.as_view(), {}, "gallery_view"),
     (r'^create-album/(?P<pk>\d+)/$', CreateAlbum.as_view(), {}, "album_create_view"),
     (r'^update-album/(?P<pk>\d+)/$', UpdateAlbum.as_view(), {}, "album_update_view"),
)
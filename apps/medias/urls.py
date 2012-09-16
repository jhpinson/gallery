from django.conf.urls.defaults import patterns, include, url
from medias.views.medias import GenerateThumbnail, LazyThumbnail


urlpatterns = patterns('',
    (r'^thumbnail/generate/(?P<pk>\d+)/(?P<size>.+)/$', GenerateThumbnail.as_view(), {}, "generate_thumbnail_view"),
    (r'^thumbnail/lazy/(?P<pk>\d+)/(?P<size>.+)/$', LazyThumbnail.as_view(), {}, "lazy_thumbnail_view"),
    
)


from django.conf.urls.defaults import patterns
from .views.albums import AlbumView, GalleryView, CreateAlbum, UpdateAlbum


urlpatterns += patterns('',
    (r'^$', AlbumView.as_view(), {}, "home_view"),
    (r'^(?P<pk>\d+)/$', AlbumView.as_view(), {}, "album_view"),
     (r'^gallery/(?P<pk>\d+)/$', GalleryView.as_view(), {}, "gallery_view"),
     (r'^create-album/(?P<pk>\d+)/$', CreateAlbum.as_view(), {}, "album_create_view"),
     (r'^update-album/(?P<pk>\d+)/$', UpdateAlbum.as_view(), {}, "album_update_view"),
)
from django.conf.urls.defaults import patterns, include, url
from medias.views.medias import GenerateThumbnail, LazyThumbnail, MediaView,\
    ModalVideoView, AlbumMediaView
from medias.views.albums import SearchAlbum
from medias.views.rest import RestMediaView
from django.views.generic.base import TemplateView
from medias.views.upload import UploadView


urlpatterns = patterns('',
    
    url(RestMediaView.make_url(), RestMediaView.as_view(), name='rest_media_view'),
                       
    (r'^p/thumbnail/generate/(?P<pk>\d+)/(?P<size>.+)/$', GenerateThumbnail.as_view(), {}, "generate_thumbnail_view"),
    (r'^p/thumbnail/lazy/(?P<pk>\d+)/(?P<size>.+)/$', LazyThumbnail.as_view(), {}, "lazy_thumbnail_view"),
    
    (r'^p/upload/$', UploadView.as_view(), {}, "upload_view")
)

"""
from django.conf.urls.defaults import patterns
from .views.albums import AlbumView, GalleryView, CreateAlbum, UpdateAlbum


urlpatterns += patterns('',
    (r'^$', AlbumView.as_view(), {}, "home_view"),
    (r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), {}, "album_view"),
     (r'^gallery/(?P<pk>\d+)/$', GalleryView.as_view(), {}, "gallery_view"),
     (r'^create-album/(?P<pk>\d+)/$', CreateAlbum.as_view(), {}, "album_create_view"),
     (r'^create-album/$', CreateAlbum.as_view(), {}, "album_create_view"),
     (r'^update-album/(?P<pk>\d+)/$', UpdateAlbum.as_view(), {}, "album_update_view"),
     (r'^media/(?P<pk>\d+)/$', MediaView.as_view(), {}, "media_view"),
     (r'^album-media/(?P<pk>\d+)/$', AlbumMediaView.as_view(), {}, "album_media_view"),
     (r'^modal-video/(?P<pk>\d+)/$', ModalVideoView.as_view(), {}, "modal_video_view"),
     (r'^autocomplete-album/$', SearchAlbum.as_view(), {}, "autocomplete_album_view"),
     
)"""
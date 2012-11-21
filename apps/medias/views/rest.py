from helpers.rest.views import BackboneView
from ..models import Media
import json

class RestMediaView(BackboneView):
    model = Media
    url_root = "rest/medias"
    
    
    def get_ancestors(self):
        
        ancestors = []
        
        ancestor = self.model.objects.get(pk=self.kwargs.get('oid'))
        while (ancestor is not None):
            ancestors.insert(0, ancestor.toJSON())
            ancestor = ancestor.parent_album
        
        return json.dumps(ancestors)
            
    def get_filters(self):
        filter = {}
        
        if self.request.GET.get('is_an_album', None) is not None:
            filter['is_an_album'] = self.request.GET.get('is_an_album', None)
             
        if self.request.GET.get('parent_album_id', None) is not None:
            filter['parent_album_id'] = self.request.GET.get('parent_album_id', None)
            
                
        return filter